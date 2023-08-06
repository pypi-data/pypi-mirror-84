import boto3
import moto
import os.path
import pathlib
import tempfile
import falcon_helpers.contrib.storage as storage


def document_from_temp(temp):
    return storage.Document(
        name=temp.name,
        uid=os.path.basename(temp.name),
        storage_type='local',
        path=temp.name,
        details={}
    )


class TestS3FileStore:
    @moto.mock_s3
    def test_warning_message_writes_when_passing_mode(self, caplog):
        s3 = boto3.resource('s3')
        s3.create_bucket(Bucket='bucket')
        obj = s3.Object('bucket', key='path')
        obj.put(Body='content')

        doc = storage.Document('name', 'uid', 'path')
        store = storage.S3FileStore('bucket')
        data = store.fetch_fp(doc, mode='rb')
        assert data.read() == b'content'
        assert 'S3FileStore' in caplog.records[0].message


class TestLocalFileStore:
    def test_fetching_a_file_by_fp(self):
        with tempfile.TemporaryDirectory() as d:
            store = storage.LocalFileStore(d, uidgen=lambda: 'unique-name')

            with tempfile.NamedTemporaryFile(prefix=d) as rf:
                rf.write(b'test')
                rf.seek(0)

                doc = document_from_temp(rf)
                fp = store.fetch_fp(doc)
                with fp as f:
                    assert f.read() == b'test'

    def test_save_does_not_require_path(self):
        with tempfile.TemporaryDirectory() as d:
            store = storage.LocalFileStore(d, uidgen=lambda: 'unique-name')

            with tempfile.NamedTemporaryFile(prefix=d) as f:
                doc = store.save(f.name, f)
                assert doc.uid == 'unique-name'
                assert doc.name == f.name
                assert doc.path == str(pathlib.Path(d).joinpath(doc.uid))

            with tempfile.NamedTemporaryFile(prefix=d) as f:
                doc = store.save(f.name, f, path='other')
                assert doc.uid == 'unique-name'
                assert doc.name == f.name
                assert doc.path == str(pathlib.Path(d).joinpath('other', doc.uid))
