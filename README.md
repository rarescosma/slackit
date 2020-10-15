# slackit

[![Build Status][travis-image]](https://travis-ci.org/rarescosma/slackit)

An attempt to automate toil away from the daily planning and work logs.

## Requirements

Make sure you're on python version `3.8.6`.

If using [pyenv](https://github.com/pyenv/pyenv) make sure python has been installed with shared library support, i.e. 

    $ env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.8.6


## Installing

    $ make
    $ sudo make install

### Configuration

Check out the [sample config](https://github.com/rarescosma/slackit/blob/main/config.sample.yaml).

Authentication:
* [Obtaining Slack tokens](https://github.com/erroneousboat/slack-term/wiki#running-slack-term-without-legacy-tokens)
* [Obtaining Google Docs API credentials](https://developers.google.com/docs/api/quickstart/python)

## Command line usage

    $ slackit -c <config_file> -e <event_name> [--check-date]


Couple it with any `cron` implementation by invoking the `slacker` script.

Sample `crontab`:

```
# dispatch the '<event_name>' messages at 8:45 on every workday
45 8 * * 1-5 slackit -c <config_file> -e <event_name>
```

[travis-image]: https://img.shields.io/travis/rarescosma/slackit
