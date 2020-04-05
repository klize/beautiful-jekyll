---
layout: post
published: true
title: When Pip is extremely slow
subtitle: pypi mirror in korea
date: '2020-04-05'
---

# Kakao PyPi mirror 

Pip가 너무 느리다. 하면 아무래도 받아오는 소스문제 일거다.

 `~/.pip/pip.conf` 에다가 다음내요을 적어두면 국내 미러사이트를 이용하기 때문에 왠만하면 해결될 것이다.

```ini
[global]
index-url=http://ftp.daumkakao.com/pypi/simple
trusted-host=ftp.daumkakao.com
```



