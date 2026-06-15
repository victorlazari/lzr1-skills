# `prompt` CLI Tool Command Reference

## Introduction

The `prompt` CLI tool is a powerful command-line utility designed to facilitate interaction with various systems and services through prompts and responses. It allows users to automate tasks, script interactions, and integrate with APIs seamlessly. This document provides a comprehensive guide to the commands, flags, and options available in the `prompt` tool.

---

## Command Structure

The general structure for executing commands with the `prompt` CLI tool is as follows:

```shell
prompt [command] [options] [arguments]
```

- **command**: Specifies the action to be performed.
- **options**: Modifies the behavior of commands.
- **arguments**: Provides additional information required by commands.

---

## Global Options

These options can be applied to any command.

- `-h`, `--help`: Display help information about the command.
- `-v`, `--version`: Output the version number of the `prompt` tool.
- `--config <path>`: Specify a custom configuration file.
- `--verbose`: Enable verbose output for debugging purposes.
- `--quiet`: Suppress output, only errors will be shown.

---

## Commands

### `init`

Initializes a new prompt configuration or updates an existing one.

#### Usage

```shell
prompt init [options]
```

#### Options

- `--overwrite`: Overwrite an existing configuration without prompting.
- `-d`, `--directory <dir>`: Specify the directory for configuration files.

#### Examples

```shell
prompt init --overwrite
prompt init -d ~/my_prompts
```

### `run`

Executes a specified prompt script.

#### Usage

```shell
prompt run [options] <script>
```

#### Options

- `-p`, `--parameter <key=value>`: Pass parameters to the script.
- `-e`, `--env <key=value>`: Set environment variables for the script.
- `--dry-run`: Simulate the execution without running the script.

#### Arguments

- `<script>`: The path to the script to be executed.

#### Examples

```shell
prompt run my_script.prompt
prompt run -p user=admin -e ENV=production my_script.prompt
```

### `list`

Lists available prompt scripts or configurations.

#### Usage

```shell
prompt list [options]
```

#### Options

- `-a`, `--all`: List all scripts, including hidden ones.
- `-d`, `--directory <dir>`: Specify the directory to list scripts from.

#### Examples

```shell
prompt list
prompt list -a
prompt list -d ~/my_prompts
```

### `validate`

Validates the syntax and structure of a prompt script.

#### Usage

```shell
prompt validate [options] <script>
```

#### Options

- `--strict`: Enable strict validation mode.
- `--format <format>`: Specify the output format (json, text).

#### Arguments

- `<script>`: The path to the script to be validated.

#### Examples

```shell
prompt validate my_script.prompt
prompt validate --strict --format json my_script.prompt
```

### `convert`

Converts prompt scripts between different formats.

#### Usage

```shell
prompt convert [options] <source> <destination>
```

#### Options

- `-f`, `--from <format>`: Specify the source format.
- `-t`, `--to <format>`: Specify the destination format.
- `--backup`: Create a backup of the original file.

#### Arguments

- `<source>`: The path to the source script.
- `<destination>`: The path where the converted script will be saved.

#### Examples

```shell
prompt convert -f json -t yaml my_script.json my_script.yaml
prompt convert --backup my_script.prompt my_script.bak
```

### `config`

Displays or modifies the configuration settings for the `prompt` tool.

#### Usage

```shell
prompt config [options] [key] [value]
```

#### Options

- `--set <key=value>`: Set a configuration key to a specific value.
- `--get <key>`: Retrieve the value of a configuration key.
- `--list`: List all configuration settings.

#### Arguments

- `[key]`: The configuration key to be modified or retrieved.
- `[value]`: The value to set for the configuration key.

#### Examples

```shell
prompt config --set timeout=30
prompt config --get timeout
prompt config --list
```

### `help`

Displays help information for commands and options.

#### Usage

```shell
prompt help [command]
```

#### Arguments

- `[command]`: The command to display help information for.

#### Examples

```shell
prompt help run
prompt help
```

---

## Advanced Usage

### Environment Variables

The `prompt` tool can utilize environment variables to customize its behavior. Some common environment variables include:

- `PROMPT_HOME`: Specifies the home directory for prompt scripts.
- `PROMPT_LOG_LEVEL`: Sets the logging level (e.g., DEBUG, INFO, WARN, ERROR).

### Scripting and Automation

The `prompt` tool is designed to be easily integrated into scripts and automation workflows. By using options like `--dry-run` and `--verbose`, users can ensure safe and informative execution of scripts in automated environments.

### Error Handling

The `prompt` tool follows standard exit codes to indicate success or failure:

- `0`: Success
- `1`: General error
- `2`: Misuse of shell builtins (e.g., invalid command or option)

---

## Configuration File

The configuration file for the `prompt` tool is typically located at `~/.prompt/config.json`. Users can customize settings such as default directories, logging preferences, and more.

### Sample Configuration

```json
{
  "default_directory": "~/prompts",
  "log_level": "INFO",
  "timeout": 60
}
```

### Modifying Configuration

Users can directly edit the configuration file or use the `prompt config` command to make changes.

---

## Conclusion

The `prompt` CLI tool provides a versatile and powerful interface for interacting with various systems through prompts. With its extensive set of commands and options, users can customize their workflows and automate complex tasks effectively. This documentation serves as a comprehensive guide for utilizing the full potential of the `prompt` tool.