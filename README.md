
# Welcome to your CDK Python project - DocxToPdfConverter.

This is a CDK Python project to create Source S3 bucket to upload docx, which will trigger AWS Lambda to convert it into PDF file, which is uploaded in another PDF Destination S3 bucket.


Steps to Deploy this project in AWS Account.

1. Recommend to use AWS Cloud9 workspace with user who has necessary permissions to create S3 buckets, AWS Lambda and necessry IAM Roles.
2. Go to AWS Lambda and create a new Layer with uploading the given brotlipy-layer.zip file, name it as "brotlipy-layer". Please update the ARN value in "py_docxtopdf_stack.py" file to replace value for brotlipy_layer_arn (Line#23)
3. Follow below steps to create the python3 virtual environment and deploy the CDK Project.
4. Post the project is deployed, go to S3 buckets and search for bucket name with "*docxsrc*", upload ".docx" file and then you can check output bucket name with *pdfdest* for converted ".pdf" file.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

Deploy the CDK to AWS Account.


```
$ cdk deploy
```

Output 

....

 ✅  PyDocxtopdfStack

✨  Deployment time: 71.42s

Stack ARN: <<STACK ARN>>

✨  Total time: 78.21s


## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!

Referred Blog: [Convert Doc or Docx to pdf using AWS Lambda](https://medium.com/analytics-vidhya/convert-word-to-pdf-using-aws-lambda-cb111be0d685) by @kuharan
