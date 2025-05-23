import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Arguments passed to the job
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'sourcepath', 'targetpath'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
logger = glueContext.get_logger()

job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read CSV from source path in S3
df = spark.read.option("header", True).csv(args['sourcepath'])
logger.info(f"csv record count : {df.count()}")

# OPTIONAL: Transform or clean data
# Example: df = df.dropDuplicates()

# Write CSV to target path
df.write.mode("overwrite").option("header", True).parquet(args['targetpath'])
df_parquet = spark.read.parquet(args['targetpath'])
parquet_count = df_parquet.count()
logger.info(f"Parquet record count at {args['targetpath']}: {parquet_count}")

job.commit()
