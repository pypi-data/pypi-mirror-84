# Pipeline Runner

When running, the configuration folder should have the following structure
```
  example_configuration_folder
├──   pipelines.yaml
├──   variables.yaml
├──   functions.py
├──   templates
│  ├──   script.jinja2
│  ├──   singularity.jinja2
│  ├──   etc.jinja2

```

## pipelines.yaml
The root element should be a dictionary in which the **keys** = pipeline names,
the **values** = an array of tasks to run.

You can use the variables within the values by prefixing with a dollar sign
(`$`), similar to shell expansions. You can escape `$` by doubling it to `$$`

For a full example look at [example/pipelines.yaml](example/pipelines.yaml). The possible tasks are:

### set_from_env: dict
Typically used in the beginning, used to define variables based on values
from environment variables.
Example:

```yaml
- set_variables:
    USER: steve
    HOME: /scratch/$USER/home/
```
### set_variables: dict
Directly define or override specific variables.
Example:

```yaml
- set_variables:
    NEW_VARIABLE: Superman
    VAR2: True
```
### load_variables: str
This will load the flat dictionary of key str. Example:
```yaml
- load_variables: pipeline_one
```

### dump_variables: filename
This will dump all of the current variables into a file, specified by filename. Example:
```yaml
- dump_variables: $SUBJECT/${SESSION}.sh
# Assumming SUBJECT + SESSION have been defined in a prior step
```

### generate_file: dict
Create a file from a Jinja2 template. This step accepts a yaml dictionary
with the following key-value pairs:
<dl>
  <dt>template</dt>
  <dd>The Jinja2 template file to use relative to the <b>configuration_dir/templates/</b></dd>
  <dt>filepath</dt>
  <dd>The full path onto which the new file should be saved to. </dd>
  <dt>variable</dt>
  <dd>The dynamic value of filepath is converted to a static absolute path and
  saved to the specifed variable. The default value = "<b>OUTPUT_FILE</b>".</dd>
</dl>

Example:

```yaml
- generate_file:
    template: script.jinja2
    filepath: $WORKING_DIR/$SUBJECT/$SESSION_PROCESSING.sh
    variable: PROCESSING_SCRIPT
# now $PROCESSING_SCRIPT can be used in a future step
# for example, a function that adds the script on the PBS queue
```
### function: str
The function to call. Note: The functions must be defined in `configuration_dir/functions.py`
Example:

```yaml
- function: load_scripts_onto_pbs
```