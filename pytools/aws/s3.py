import os

import boto3
from rich import print
from rich.progress import Progress


def set_profile(profile):
	boto3.setup_default_session(profile_name=profile)


def reset_profile():
	boto3.setup_default_session(profile_name='default')


def get_buckets(profile=None):
	if profile is not None:
		set_profile(profile)
	s3_resource = boto3.resource('s3')

	for bucket in s3_resource.buckets.all():
		print(bucket.name)

	reset_profile()


def upload_file(source, bucket, filename, profile=None):
	if profile is not None:
		set_profile(profile)
	s3_resource = boto3.client('s3')
	s3_resource.upload_file(source, bucket, filename)
	reset_profile()


def delete_file(bucket, filename, profile=None):
	if profile is not None:
		set_profile(profile)
	s3_resource = boto3.resource('s3')
	s3_resource.Object(bucket, filename).delete()
	reset_profile()


def delete_folder(bucket, folder, profile=None):
	print(f"[red]Deleting folder: [cyan]{folder} [red]From bucket: [cyan]{bucket}")
	if profile is not None:
		set_profile(profile)
	s3_resource = boto3.resource('s3')
	bucket = s3_resource.Bucket(bucket)
	bucket.objects.filter(Prefix=folder).delete()
	reset_profile()


def upload_folder(source, bucket, location, profile=None):
	files = []
	folderName = source[source.rindex("/") + 1:]
	for (dirpath, dirnames, filenames) in os.walk(source):
		for file in filenames:
			files.append(dirpath + "/" + file)

	with Progress() as progress:
		task = progress.add_task(f"[green]Copying folder: [cyan]{folderName} [green]To bucket: [cyan]{bucket}")
		for file in files:
			print(f"[yellow]Uploading: [cyan]{file[len(source) + 1:]}")
			upload_file(file, bucket, location + folderName + file[len(source):], profile)
			progress.update(task, advance=100 / len(files))
