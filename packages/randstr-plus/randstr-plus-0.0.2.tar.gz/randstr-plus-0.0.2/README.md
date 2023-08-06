<h1 align="center">randstr-plus</h1>
<h3 align="center">A slightly more flexible string generator</h3>
<p align="center">
  <a href="https://github.com/garytyler/randstr-plus/actions">
    <img alt="Actions Status" src="https://github.com/garytyler/randstr-plus/workflows/tests/badge.svg">
  </a>

  <a href="https://codecov.io/gh/garytyler/randstr-plus">
    <img src="https://codecov.io/gh/garytyler/randstr-plus/branch/master/graph/badge.svg?token=3N9UKA0AHY" />
  </a>
  <a href="https://pypi.org/project/randstr-plus/">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/randstr-plus">
  </a>
  <a href="https://pypi.org/project/randstr-plus/">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/randstr-plus">
  </a>
  <img alt="GitHub" src="https://img.shields.io/github/license/garytyler/randstr-plus">
  <a href="https://github.com/psf/black">
    <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
  </a>
</p>

## Functions

<td style="color: #444;">
  <dl style="color: #666;">
    <dt><a name="-randstr"><h4><b>randstr</b></a>(min_length: int = 5, max_length: int =
      25, min_tokens: int = 1, max_tokens: int = 5, lowercase_letters: bool = True,
      uppercase_letters: bool = True, punctuation: bool = True, numbers: bool = True) -&gt;
      str<h4></dt>
    <dd><h5>Return&nbsp;a&nbsp;single&nbsp;string&nbsp;generated&nbsp;from&nbsp;random&nbsp;characters&nbsp;according&nbsp;to&nbsp;the&nbsp;given&nbsp;parameters.<br>
        &nbsp;<br>
        Keyword&nbsp;Arguments:<br>
        &nbsp;&nbsp;&nbsp;&nbsp;min_length&nbsp;{int}&nbsp;--&nbsp;minimum&nbsp;total&nbsp;character&nbsp;length&nbsp;(default:&nbsp;{5})<br>
        &nbsp;&nbsp;&nbsp;&nbsp;max_length&nbsp;{int}&nbsp;--&nbsp;maximum&nbsp;total&nbsp;character&nbsp;length&nbsp;&nbsp;(default:&nbsp;{25})<br>
        &nbsp;&nbsp;&nbsp;&nbsp;min_tokens&nbsp;{int}&nbsp;--&nbsp;minimum&nbsp;total&nbsp;tokens/words&nbsp;(default:&nbsp;{1})<br>
        &nbsp;&nbsp;&nbsp;&nbsp;max_tokens&nbsp;{int}&nbsp;--&nbsp;maximum&nbsp;total&nbsp;tokens/words&nbsp;(default:&nbsp;{5})<br>
        &nbsp;&nbsp;&nbsp;&nbsp;lowercase_letters&nbsp;{bool}&nbsp;--&nbsp;allow&nbsp;lowercase&nbsp;letters&nbsp;(default:&nbsp;{True})<br>
        &nbsp;&nbsp;&nbsp;&nbsp;uppercase_letters&nbsp;{bool}&nbsp;--&nbsp;allow&nbsp;uppercase&nbsp;letters&nbsp;(default:&nbsp;{True})<br>
        &nbsp;&nbsp;&nbsp;&nbsp;punctuation&nbsp;{bool}&nbsp;--&nbsp;allow&nbsp;punctuation&nbsp;characters&nbsp;(default:&nbsp;{True})<br>
        &nbsp;&nbsp;&nbsp;&nbsp;numbers&nbsp;{bool}&nbsp;--&nbsp;allow&nbsp;numbers&nbsp;(default:&nbsp;{True})<br>
        &nbsp;<br>
        Returns:<br>
        &nbsp;&nbsp;&nbsp;&nbsp;str&nbsp;--&nbsp;generated&nbsp;string</h5></dd>
  </dl>
</td>
