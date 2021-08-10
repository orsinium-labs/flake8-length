# flake8-length

[Flake8](https://gitlab.com/pycqa/flake8) plugin for a smart line length validation.

[pycodestyle](https://github.com/PyCQA/pycodestyle) linter (used in Flake8 under the hood by default) already has `E501` and `W505` rules to validate the line length. flake8-length provides an alternative check that is smarter and more forgiving.

What is allowed:

+ Long string literals.
+ Long URLs in strings and comments.
+ When the last word in a text doesn't fit a bit.

## Motivation

From [linux code style](https://github.com/torvalds/linux/blob/master/Documentation/process/coding-style.rst#2-breaking-long-lines-and-strings):

> Statements longer than 80 columns will be broken into sensible chunks, unless exceeding 80 columns significantly increases readability and does not hide information. <...> However, never break user-visible strings such as printk messages, because that breaks the ability to grep for them.

I see a lot of Python code that does some awful breaks to fit long text messages into the project's line limit just because. However, it creates a lot of difficulties:

1. Difficult to grep.
1. Easy to miss a space on the string breaks.
1. It doesn't make code more readable at all, even decreases readability. In most cases, I don't care if the ending of an error message goes outside of my screen.

Some modern languages even don't have this limitation:

> Go has no line length limit. Don't worry about overflowing a punched card.

However, it makes sense to keep some limit to guide developers and keep the alignment reasonable.

[Uncle Bob analyzed line length in some popular Java project](https://youtu.be/2a_ytyt9sf8?t=2792). The conclusion is it is usually about 45 on average, more than 97 is too much and exceptional.

[Raymond Hettinger advises to keep it 90ish](https://youtu.be/wf-BqAjZb8M?t=260). The limit should be about 90 but with reasonable exceptions for when breaking the line would negatively affect the readability.

[Kevlin Henney says even 80 is too generous](https://youtu.be/ZsHMHukIlJY?t=716). People read the code following one up-down flow, and breaking the flow with long lines makes the code harder to read.

If you ever had to break a text message to fit in the limit, you know why the plugin exists.

If you're about having as strict limits as possible, flake8-length is on your side. It's better to set 90 chars limit with a few reasonable exceptions rather than have 120 or more chars limit for everything.

## Installation

Install:

```bash
python3 -m pip install --user flake8-length
```

And check if the plugin is detected by flake8:

```bash
flake8 --version
```

If it doesn't, flake8-length was installed in another python interpreter rather than flake8. You can find the right one:

```bash
head -1 $(which flake8)
```

## Usage

+ If you're installed flake8-length and flake8 in the same environment, when you run flake8 it will run the plugin. Just give it a try.
+ pycodestyle has a few hard limits on lime length (`E501` and `W505`), so these checks should be disabled to avoid conflicts with flake8-length.
+ The default soft limit is set using [max-line-length](https://flake8.pycqa.org/en/latest/user/options.html#cmdoption-flake8-max-line-length) option. It is 79 by default.

Configuration example (`setup.cfg`):

```ini
[flake8]
extend-ignore =
    E501,
    W505
max-line-length = 90
```

What the limit you should use? I'd say, as small as possible. Try to start with the default one (79) and if you feel it's not enough, extend it to 90. More is too generous.
