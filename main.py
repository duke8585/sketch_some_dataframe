from inspect import cleandoc
from csv import DictReader
from pprint import pprint as pp


def read_input(filepath="input.tsv") -> tuple[list[str], list[list]]:
  """read tsv file and return field names header + the rows as list of list"""
  with open("input.tsv", "r") as ipf:
    sipf = [
      line for line in ipf.read().splitlines()
      if not line.startswith("#") and not line == ""
    ]
    dict_reader = DictReader(sipf, delimiter="\t")
    # ipf.close()
    field_names = dict_reader.fieldnames
    rows = [list(i.values()) for i in dict_reader]

  return field_names, rows


def prep_item(item: str, quotes="\""):
  """empty string to null else string escaped"""
  if len(item) == 0:
    return "null"
  else:
    return f"{quotes}{item}{quotes}"


def prep_col(colname: str, quotes="\""):
  """allow for constants à la C.COL_NAME unescaped by quote"""
  if "." in colname:
    return f"{colname}"
  else:
    return f"{quotes}{colname}{quotes}"


def make_data_rows(rows, nof_rows, nof_cols, br="[]", q="\""):
  """make test rows from list of list with values"""
  data = []
  data.append(br[0])  # open ([
  for r_n, row in enumerate(rows):
    data.append("(")  # always (
    for i_n, item in enumerate(row):
      if i_n + 1 < nof_cols:
        data.append(f"{prep_item(item, quotes=q)}, ")
      else:
        data.append(f"{prep_item(item, quotes=q)}")
    if r_n + 1 < nof_rows:
      data.append(f"),")  # always )
    else:
      data.append(")")  # always )
    data.append("\n")
  data.append(br[1])  # close )]
  return "".join(data)


def make_schema(field_names, nof_cols, br="[]", q="\""):
  """make schema with field names"""
  schema = []
  schema.append(br[0])  # open ([
  for i_c, col in enumerate(field_names):
    if i_c + 1 < nof_cols:
      schema.append(f"{prep_col(col, quotes=q)}, ")
    else:
      schema.append(f"{prep_col(col, quotes=q)}")
  schema.append(br[1])  # close )]
  return "".join(schema)


def make_generation_statements(field_names, rows, nof_rows, nof_cols):
  """template a body with all three flavors, scala spark, pyspark and SQL values"""
  body = []
  body.append("/** +++++ scala spark df definition */")
  body.append("\n")
  body.append(
    "// val conf = new SparkConf().setAppName(\"someExample\").setMaster(\"local[1]\")"
  )
  body.append("\n")
  body.append(
    "// val spark = SparkSession.builder().config(conf).appName(\"someExample\").master(\"local\").getOrCreate()"
  )
  body.append("\n")
  body.append("// import spark.implicits._")
  body.append("\n")
  body.append("// format: off")
  body.append("\n")
  body.append("val df = Seq")
  body.append(make_data_rows(rows, nof_rows, nof_cols, br="()", q="\""))
  body.append(".toDF")
  body.append(make_schema(field_names, nof_cols, br="()", q="\""))
  body.append("\n")
  body.append("// format: on")
  with open('output.sc', 'w') as out_file:
    out_file.write("".join(body))

  ##
  ##
  body = []
  body.append("# +++++ py spark df definition")
  body.append("\n")
  body.append(
    cleandoc("""
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
    # )"""))
  body.append("\n")
  body.append("data = ")
  body.append(make_data_rows(rows, nof_rows, nof_cols, br="[]", q="\""))
  body.append("\n")
  body.append("schema = ")
  body.append(make_schema(field_names, nof_cols, br="[]", q="\""))
  body.append("\n")
  body.append("df = spark.createDataFrame(data).toDF(*schema)")
  body_cleaned = "".join(body).replace("null", "None")
  with open('output.py', 'w') as out_file:
    out_file.write(body_cleaned)

  ##
  ##
  body = []
  body.append("-- +++++ SQL values table definition")
  body.append("\n")
  body.append("with base as (")
  body.append("\n")
  body.append("select * from (")
  body.append("\n")
  body.append("values")
  body.append("\n")
  body.append(make_data_rows(rows, nof_rows, nof_cols, br="  ",
                             q="\'"))  # NOTE ugly br for SQL but works
  body.append(") AS t")
  body.append(make_schema(field_names, nof_cols, br="()", q=""))
  body.append(")")
  body.append("\nselect * from base")
  with open('output.sql', 'w') as out_file:
    out_file.write("".join(body))


if __name__ == "__main__":
  field_names, rows = read_input()
  nof_rows = len(rows)
  nof_cols = len(field_names)
  make_generation_statements(field_names, rows, nof_rows, nof_cols)
