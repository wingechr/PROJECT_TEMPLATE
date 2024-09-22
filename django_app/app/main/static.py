import logging

from django.contrib.staticfiles.storage import ManifestStaticFilesStorage


class ManifestStaticFilesStorageWithIgnore(ManifestStaticFilesStorage):
    def post_process(self, paths: dict, dry_run=False, **options):
        for original_path, processed_path, processed in super().post_process(
            paths, dry_run=dry_run, **options
        ):
            if isinstance(processed, Exception):
                logging.warning(
                    f"ManifestStaticFilesStorage {original_path}: {processed}"
                )
                continue
            yield original_path, processed_path, processed
