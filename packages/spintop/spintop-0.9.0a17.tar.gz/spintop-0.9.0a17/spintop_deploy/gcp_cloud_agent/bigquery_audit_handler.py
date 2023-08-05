from google.cloud import bigquery

from spintop_deploy.pub_sub_router import BigQueryJobHandler, BigQueryAuditLogMessage, PubSubRouter

def bigquery_audit_handler(spintop_client, bq_client=None):
    
    if bq_client is None:
        bq_client = bigquery.Client()
    @BigQueryJobHandler
    def handle_bq_message(message: BigQueryAuditLogMessage):
        if message.table_id == 'spintop_metadata':
            table_identifier = f'`{message.project_id}`.`{message.dataset_id}`.`{message.table_id}`'
            metadata_result = bq_client.query(f'SELECT * FROM {table_identifier}').result()

            for index, row in enumerate(metadata_result):
                # Only one row expected.
                if index > 0:
                    raise ValueError(f'Metadata returned more rows than expected (1)')

                metadata = row

            spintop_client.update_spintop_metadata(metadata)

            return True
        else:
            return False

    router = PubSubRouter([handle_bq_message])
    return router.request_handler()
