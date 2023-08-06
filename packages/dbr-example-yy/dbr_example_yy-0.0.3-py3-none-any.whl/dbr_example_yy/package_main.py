from argparse import ArgumentParser

def run():
    parser = ArgumentParser()
    parser.add_argument('storate_account_name', nargs='+')
    parser.add_argument('storage_scope', nargs='+')
    parser.add_argument('storage_key', nargs='+')
    parser.add_argument('src_blob_container', nargs='+')
    parser.add_argument('dst_blob_container', nargs='+')
    args = parser.parse_args()
    from folder import some_file
    some_file.test(args)
