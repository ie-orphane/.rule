# .rule

## instalation

**Requires python 3.8+**

```shell
git clone ~/.rule
echo "alias .rule=\"python3 -u ~/.rule $@\"" >> $HOME/.${SHELL##*/}rc
```

## Usage

- Runs on the current directory and any sub-directory:

```shell
.rule
```

- Runs on the given filename(s):

```shell
.rule script.sh
```
