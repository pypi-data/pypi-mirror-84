import json
import logging
import google.auth
from google.cloud import firestore
from google.cloud import firestore_admin_v1
from pyinsight import depositor
from pyinsight.utils.core import get_current_timestamp, encoder

class FirestoreDepositor(depositor.Depositor):
    db = None
    topic_object = None
    data_encode = 'gzip'

    def _get_filter_key(self, merge_status, merge_level):
        """
        Firestore accept an IN statement of 10. We must cut the request:
        9: Header
        8 Packaged
        7: merged : merge_level >= 3
        4-6: merged: merge level 0-2
        3: initial : merge_level >= 3
        0-2: initial : merge_level 0-2
        """
        if merge_status == 'header':
            return 9
        elif merge_status == 'packaged':
            return 8
        elif merge_status == 'merged':
            return 4 + min(3, merge_level)
        elif merge_status == 'initial':
            return min(3, merge_level)

    def set_connection(self, db: firestore.Client):
        self.db = db

    def init_topic(self, topic_id):
        """
        Admin Client Reference:
        API: https://googleapis.dev/python/firestore/latest/admin_client.html
        Protocol: https://cloud.google.com/firestore/docs/reference/rpc/google.firestore.admin.v1
        """
        project_id = google.auth.default()[1]
        dbadmin = firestore_admin_v1.FirestoreAdminClient()
        parent = '/'.join(['projects', project_id, 'databases', '(default)', 'collectionGroups', topic_id])
        data_path = '/'.join([parent, 'fields', 'data'])
        asc_index = {"name": topic_id + "-idx-asc", "query_scope": "COLLECTION",
                 "fields": [{"field_path": "table_id", "order": "ASCENDING"},
                            {"field_path": "filter_key", "order": "ASCENDING"},
                            {"field_path": "sort_key", "order": "ASCENDING"}]}
        desc_index = {"name": topic_id + "idx-desc", "query_scope": "COLLECTION",
                 "fields": [{"field_path": "table_id", "order": "ASCENDING"},
                            {"field_path": "filter_key", "order": "ASCENDING"},
                            {"field_path": "sort_key", "order": "DESCENDING"}]}
        data_field = {"name": data_path, "index_config": {"indexes": []}}
        create_asc_index = dbadmin.create_index(parent, asc_index)
        logging.info("{}: Ascending Index Creation".format(topic_id))
        create_desc_index = dbadmin.create_index(parent, desc_index)
        logging.info("{}: Descending Index Creation".format(topic_id))
        update_field = dbadmin.update_field(data_field)
        logging.info("{}: Removing Index of field Data".format(topic_id))

    def set_current_topic_table(self, topic_id, table_id):
        self.topic_id = topic_id
        self.table_id = table_id
        self.topic_object = self.db.collection(topic_id)

    # Sorted key must be added here
    def add_document(self, header, data) -> bool:
        self.set_current_topic_table(header['topic_id'], header['table_id'])
        content = header.copy()
        # Encoder
        if content['data_store'] == 'body':
            if isinstance(data, list):
                content['data'] = encoder(json.dumps(data), content['data_encode'], self.data_encode)
            else:
                content['data'] = encoder(data, content['data_encode'], self.data_encode)
            content['data_encode'] = self.data_encode
        else:
            content['data'] = data
        # Case 1 : Header
        if str(content.get('age', '')) == '1':
            content['age'] = 1
            content['aged'] = content.get('aged', '') == 'true'
            content['sort_key'] = content['start_seq']
        # Case 2 : Aged Document
        elif 'age' in content:
            for key in [k for k in ['age', 'end_age', 'segment_start_age'] if k in content]:
                content[key] = int(content[key])
                content['sort_key'] = content['merge_key']
        # Case 3 : Normal Document
        else:
            content['deposit_at'] = get_current_timestamp()
            content['sort_key'] = content['deposit_at']
        # Save Document
        try:
            content['filter_key'] = self._get_filter_key(content['merge_status'], content['merge_level'])
            self.topic_object.add(content)
        except Exception as e:
            logging.error("{}: {}".format(self.topic_id, e))
            return False
        return True

    def update_document(self, ref: firestore.DocumentSnapshot, data) -> bool:
        # Update Document
        try:
            data['filter_key'] = self._get_filter_key(data['merge_status'], data['merge_level'])
            ref.reference.update(data)
        except Exception as e:
            logging.error("{}: {}".format(self.topic_id, e))
            return False
        return True

    def delete_documents(self, ref_list) -> bool:
        ok_flag = True
        for ref in ref_list:
            try:
                ref.reference.delete()
            except Exception as e:
                logging.error("{}: {}".format(self.topic_id, e))
                ok_flag = False
                continue
        return ok_flag

    def get_table_header(self):
        for ref in self.get_stream_by_sort_key(['header'], reverse=True):
            return ref

    def get_ref_by_merge_key(self, merge_key) -> firestore.DocumentSnapshot:
        q = self.topic_object.where('table_id', '==', self.table_id).where('merge_key', '==', merge_key).limit(1)
        for ref in q.stream():
            return ref

    def get_dict_from_ref(self, ref) -> dict:
        return ref.to_dict()

    def get_stream_by_sort_key(self, status_list=None, le_ge_key=None, reverse=False,
                               min_merge_level=0, equal=True):
        white_list = list()
        initial_merge_level_dict = {x: [i for i in range(4) if i >= x] for x in range(4)}
        merged_merge_level_dict = {x + 4: [i + 4 for i in range(4) if i >= x] for x in range(4)}
        if not status_list:
            status_list = ['header', 'initial', 'merged', 'packaged']
        if 'initial' in status_list:
            white_list.extend(initial_merge_level_dict.get(min_merge_level))
        if 'merged' in status_list:
            white_list.extend(merged_merge_level_dict.get(min_merge_level + 4))
        if 'packaged' in status_list:
            white_list.append(8)
        if 'header' in status_list:
            white_list.append(9)
        if reverse:
            if not le_ge_key:
                q = self.topic_object.where('table_id', '==', self.table_id) \
                                     .where('filter_key', 'in', white_list) \
                                     .order_by('sort_key', direction=firestore.Query.DESCENDING)
            elif equal:
                q = self.topic_object.where('table_id', '==', self.table_id) \
                    .where('filter_key', 'in', white_list) \
                    .where('sort_key', '<=', le_ge_key).order_by('sort_key', direction=firestore.Query.DESCENDING)
            else:
                q = self.topic_object.where('table_id', '==', self.table_id) \
                    .where('filter_key', 'in', white_list) \
                    .where('sort_key', '<', le_ge_key).order_by('sort_key', direction=firestore.Query.DESCENDING)
        else:
            if not le_ge_key:
                q = self.topic_object.where('table_id', '==', self.table_id) \
                                     .where('filter_key', 'in', white_list) \
                                     .order_by('sort_key')
            elif equal:
                q = self.topic_object.where('table_id', '==', self.table_id) \
                    .where('filter_key', 'in', white_list) \
                    .where('sort_key', '>=', le_ge_key).order_by('sort_key')
            else:
                q = self.topic_object.where('table_id', '==', self.table_id) \
                    .where('filter_key', 'in', white_list) \
                    .where('sort_key', '>', le_ge_key).order_by('sort_key')
        for ref in q.stream():
            # Min_merge_level >= 3 means the furthur analysis is necessairy
            if min_merge_level >= 3:
                doc_dict = self.get_dict_from_ref(ref)
                if doc_dict['merge_level'] < min_merge_level:
                    continue
            yield ref

    def merge_documents(self, base_doc: firestore.DocumentSnapshot, merge_flag, start_key, end_key, data_list,
                        min_start=None, merged_level=0) -> bool:
        base_doc_dict = self.get_dict_from_ref(base_doc)
        data_operation_flag = False
        if 'age' in base_doc_dict:
            aged_flag = True
            segment_key_start = base_doc_dict.get('segment_start_age', 0)
            doc_key_start = base_doc_dict['age']
            doc_key_end = base_doc_dict.get('end_age', base_doc_dict['age'])
        else:
            aged_flag = False
            segment_key_start = base_doc_dict.get('segment_start_time', 0)
            doc_key_start = base_doc_dict.get('start_time', base_doc_dict['deposit_at'])
            doc_key_end = base_doc_dict['deposit_at']
        # Case 1: Merged Member Nodes / Leader with same min_start = Do nothing
        if base_doc_dict['merge_status'] == 'merged' and base_doc_dict['merged_level'] == merged_level:
            if not min_start or min_start == segment_key_start:
                return data_operation_flag
        # Case 2: Leader nodes, need to update min_start
        if base_doc_dict.get('merged_level', -1) != merged_level:
            base_doc_dict['merged_level'] = merged_level
        if min_start:
            if aged_flag:
                base_doc_dict['segment_start_age'] = min_start
            else:
                base_doc_dict['segment_start_time'] = min_start
        # Case 3: Check if data should be manimulated
        if doc_key_end == end_key and doc_key_start == start_key:
            pass
        elif base_doc_dict['merge_status'] == 'merged':
            pass
        else:
            base_doc_dict['data'] = encoder(json.dumps(data_list), 'flat', self.data_encode)
            data_operation_flag = True
            if aged_flag:
                base_doc_dict.update({'age': start_key, 'end_age': end_key})
            else:
                base_doc_dict.update({'start_time': start_key})
        # Case 4.1: Final Merge cases
        if merge_flag:
            base_doc_dict['merge_status'] = 'merged'
        self.update_document(base_doc, base_doc_dict)
        return data_operation_flag


if __name__=='__main__':
    db = firestore.Client()
    depositor = FirestoreDepositor()
    # depositor.set_connection(db)
    # test_add_document(depositor)
    # test_get_table_header(depositor)
    depositor.init_topic('test-001')


