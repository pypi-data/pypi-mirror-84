def test(spark, **kwargs):
    print('=============================')
    print(kwargs)
    spark.conf.set(
      'fs.azure.account.key.{}.blob.core.windows.net'.format(kwargs['storate_account_name']),
      dbutils.secrets.get(scope=kwargs['storage_scope'], key=kwargs['storage_key']))

    df = spark.read.parquet('wasbs://{}@{}.blob.core.windows.net/2020-03-03/'.format(kwargs['src_blob_container'], kwargs['storate_account_name']))
    # df = spark.read.parquet('wasbs://samplecontainer@{}.blob.core.windows.net/2020-03-03/'.format(kwargs['storate_account_name']))
    df.write.mode('overwrite').parquet('wasbs://{}@{}.blob.core.windows.net/2020-03-03/'.format(kwargs['dst_blob_container'], kwargs['storate_account_name']))
    display(df)
