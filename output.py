# +++++ py spark df definition
# from pyspark import SparkConf, SparkContext
# from pyspark.sql import SparkSession
# # spark multiple jars: https://stackoverflow.com/questions/57862801/spark-shell-add-multiple-drivers-jars-to-classpath-using-spark-defaults-conf/65799134#65799134
# conf = SparkConf()
# packages = [
#     "org.apache.hadoop:hadoop-aws:3.2.0",
#     "com.amazonaws:aws-java-sdk-bundle:1.12.370",
#     # "com.amazonaws:aws-java-sdk-s3:1.11.375", # lighter but more problems
#     # "com.amazonaws:aws-java-sdk-core:1.11.375", # lighter but more problems
# ]
# conf.set("spark.jars.packages", ",".join(packages))
# spark = SparkSession.builder.config(conf=conf).getOrCreate()
# spark._jsc.hadoopConfiguration().set(
#     "fs.s3a.aws.credentials.provider",
#     "com.amazonaws.auth.profile.ProfileCredentialsProvider",
# )
# spark._jsc.hadoopConfiguration().set(
#     "fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem"
# )
# spark._jsc.hadoopConfiguration().set(
#     "fs.s3.impl", "org.apache.hadoop.fs.s3native.NativeS3FileSystem"
# )
data = [("2022-02-01", "max", "1", None),
("2022-02-02", "max", "2", None),
("2022-02-03", "max", "3", None),
("2022-02-04", "max", "4", None),
("2022-02-01", "john", "3", None),
("2022-02-02", "john", "4", None),
("2022-02-03", "john", "5", None),
("2022-02-04", "john", "3", None),
("2022-02-05", "john", "4", None),
("2022-02-06", "john", "5", None),
("2022-02-07", "john", "6", None),
("2022-02-04", "liz", "2", None),
("2022-02-05", "liz", "3", None),
("2022-02-06", "liz", "4", None),
("2022-02-07", "liz", "5", None),
("2022-02-08", "liz", "5", None),
("2022-02-09", "liz", "8", None),
("2022-02-10", "liz", "9", None),
("2022-02-03", "liz", None, "None_allowed"),
("2022-02-04", "liz", None, "None_allowed"),
("2022-02-05", "liz", None, "None_allowed")
]
schema = ["date", "name", "debt", "remark"]
df = spark.createDataFrame(data).toDF(*schema)