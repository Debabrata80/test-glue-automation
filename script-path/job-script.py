import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Arguments passed to the job
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'SOURCE_PATH', 'TARGET_PATH'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read CSV from source path in S3
df = spark.read.option("header", True).csv(args['SOURCE_PATH'])

# OPTIONAL: Transform or clean data
# Example: df = df.dropDuplicates()

# Write CSV to target path
df.write.mode("overwrite").option("header", True).parquet(args['TARGET_PATH'])

job.commit()
