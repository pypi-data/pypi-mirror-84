
def test(args):
    spark.conf.set(
      'fs.azure.account.key.{}.blob.core.windows.net'.format(args.storate_account_name),
      dbutils.secrets.get(scope=args.storage_scope,key=args.storage_key))

    df = spark.read.parquet('wasbs://{}@{}.blob.core.windows.net/2020-03-03/'.format(args.src_blob_container, args.storate_account_name))
    # df = spark.read.parquet('wasbs://samplecontainer@{}.blob.core.windows.net/2020-03-03/'.format(args.storate_account_name))
    df.write.mode('overwrite').parquet('wasbs://{}@{}.blob.core.windows.net/2020-03-03/'.format(args.dst_blob_container, args.storate_account_name))
    display(df)
