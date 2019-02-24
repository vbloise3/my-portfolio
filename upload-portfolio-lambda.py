import json
import boto3
from botocore.client import Config
import io
import zipfile
import mimetypes


def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:001178231653:deployPortfolioTopic')

    location = {
        "bucketName": "portfoliobuild.vincebloise.com",
        "objectKey": "portfoliobuild.zip"
    }
    try:
        job = event.get("CodePipeline.job")

        if job:
            for artifact in job["data"]["inputArtifacts"]:
                if artifact["name"] == "MyAppBuild":
                    location = artifact["location"]["s3Location"]

        print ("Building portfolio from " + str(location))

        s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))

        portfolio_bucket = s3.Bucket('portfolio.vincebloise.com')
        build_bucket = s3.Bucket(location["bucketName"])

        portfolio_zip = io.BytesIO()
        build_bucket.download_fileobj(location["objectKey"], portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj, nm, ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

        print ("job done!")
        topic.publish(Subject="Portfolio Deployed", Message="Portfolio deployed successfully!")
        if job:
            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobId=job["id"])
    except:
        topic.publish(Subject="Portfolio Deploy Failed", Message="The portfolio was not deployed successfully.")
        raise
    return "hello from lambda"