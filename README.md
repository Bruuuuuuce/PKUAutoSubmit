# PKUAutoSubmit
PKU一键出入校备案小工具 v3.2 (2021.11.15)

### 听闻近期由于疫情原因恢复了报备制度，然而由于作者已毕业离校，无法访问完整的 portal 功能进行测试及维护。往后的更新基本仅来源于在校学生的 PR 并无法进行完整测试，建议 fork 后根据自身情况参考 issue 进行完善

**已知问题**：

-  `PhantomJS` 等 `driver` 问题可尝试 `chromedriver` 并取消注释 `main.py` 的相应代码
-  portal 未绑定手机时会出现错误，参考[#31](https://github.com/Bruuuuuuce/PKUAutoSubmit/issues/31)
-  最新版本 `selenium` 已停止对 `PhantomJS` 的支持， `2.48.0` 及 `3.8.0` 版本测试正常，参考[#35](https://github.com/Bruuuuuuce/PKUAutoSubmit/issues/35)
-  发行版 `v3.0` 可能出现登录问题，请采用最新 repo 或发行版，参考[#35](https://github.com/Bruuuuuuce/PKUAutoSubmit/issues/35)

### 感谢同学们的支持，祝大家一切顺利，学业有成！

为作者的第一个 `selenium` 练手小项目，完善程度较低，欢迎任意类型的使用与开发改进

## 说明

- 本工具采用 Python3 搭配 `selenium` 完成自动化操作，实现全自动填报学生出入校备案，为频繁出入校的 PKU 学子（不频繁也行）提供较为便捷的解决方案
- 支持多个配置文件，可在一个进程内同时进行多人填报
- 支持设置在运行结束后返回历史备案页面截图，无需自行登录查看备案结果
- 支持基于[Server酱](https://sct.ftqq.com/)的备案结果微信推送功能，体验更佳
- 采用定时任务可实现定期（如每日）免打扰填报
- 第三方依赖包几乎只有 `selenium` 一个，从下到用贼jr快

## 安装与需求

### Python 3

本项目需要 Python 3，可以从[Python 官网](https://www.python.org/)下载安装

本项目采用 Python 3.7.4 开发，由于含有 `f-string` ，请至少使用 Python 3.6 及以上版本，建议使用 Python 3.7 及以上版本

### Packages

#### selenium

采用如下命令安装 `selenium`，支持 2.48.0 及以上版本（注意最新版本不支持 `PhantomJS`）：

```python
pip3 install selenium==2.48.0
```

#### webdriver_manager

```
pip3 install webdriver_manager
```

然后就没了。惊不惊喜？意不意外？

## 基本用法

1. 将 `config.sample.ini` 文件重命名为 `config.ini` ，请不要新建文件，不然自己搞定编码问题

2. 用文本编辑器（建议代码编辑器）打开 `config.ini` 文件

3. 配置 `[login]` 、`[common]` 、`[out]`、`[in]`、`[capture]`、`[wechat]` 这几个 Section 下的变量，在 `config.ini` 文件内有详细注释

4. 若需要多人同时填报，可将 `config.ini` 文件复制若干份，分别重命名为 `config+序号.ini` 例如 `config1.ini`,  `config2.ini`...并配置对应变量

   **Note:** 序号仅作匹配用，具体数值不重要，但是非法命名格式可能导致检测失败

5. 进入项目根目录，以命令 `python main.py` 运行主程序
   - 亦可双击 `run.bat` 运行（仅限 Windows 系统）
   - 亦可用代码编辑器打开 `main.py` 并运行（并不推荐）

## 定时运行

### Windows

本项目中的 `autoRun.bat` 文件可提供在静默免打扰情况下运行程序的选择，配合 Windows 任务计划管理可实现定期自动填报，具体请参考[Win10下定时启动程序或脚本](https://blog.csdn.net/xielifu/article/details/81016220)

### mac OS

进入项目根目录，以命令 `./macAutoRun.sh` 执行 `macAutoRun.sh` 脚本即可，可设定或取消定时运行

### Linux

使用 Linux 系统的小伙伴们想必有一定的 shell 基础，那大佬们就自行用 `crontab` 设置吧~



**Note:** 静默运行的弊端为无法看到任何报错信息，若程序运行有错误，使用者很难得知。故建议采用定时静默运行时，设置微信推送，在移动端即可查看到备案成功信息。或设置备案历史截图功能并定期查看截图（似乎出现了问题，极不推荐）

## 利用 GitHub Actions 自动运行

fork 本仓库后，在 [config.sample.ini](config.sample.ini) 中修改除学号密码以外的参数

然后在自己仓库的 settings->secrets->New repository secret 中新建 Name 为 STUDENTNUM， Value 为学号；Name 为 passwd，Value为密码

默认每天晚上0点起每四个小时跑一次，可能会运行失败

## 微信推送

本项目支持基于[Server酱](https://sct.ftqq.com/)的微信推送功能，仅需登录并扫码绑定，之后将获取到的 SCKEY 填入 `config.ini` 文件即可

**Note:** 因微信将于4月底下线模板消息功能，届时推送功能也将同步更新为[Server酱-Turbo](https://sct.ftqq.com/)。所以有微信推送需求的小伙伴们可以提前做好准备，并关注本项目的未来版本

## 补充说明

- 本项目主要为校内日常出入的同学提供便捷解决方案，会同时填报出校与入校备案，不支持单独填报，也不支持京外返校填报。若有此类特殊需求，烦请手动填报
- `PhantomJS` 作为经典的轻量级无头浏览器，相较 `Chrome` 等大型浏览器体量小的多，不占空间且运行快速。但是由于其本身属性也可能造成一系列问题，如：
   - 由于仅为练手项目，对于学校土豆服务器造成的各类玄学问题作者只能尽力避免，但并无完善的 Exception 处理机制，若遇到报错欢迎 issue，且万能的重来一次大法可以解决绝大多数问题
   - 可能某天 `selenium` 对 `PhantomJS` 停止了支持，那到了那天再想别的办法（果然到这天了）
- 当前看来，无论出不出学校都可以填报备案，所以每天定时运行一次并没有什么问题（事实上，作者在测试阶段每天填几十次，希望人没事.jpg）

## 责任须知

- 本项目仅供参考学习，造成的一切后果由使用者自行承担
- 本项目敏感性不比 skj，利人利己，私以为还是可以合理扩散一下的，吧？

## 证书

[Apache License 2.0](https://github.com/Bruuuuuuce/PKUAutoSubmit/blob/main/LICENSE)

## 版本历史

### version 3.2

- 发布于 2021.11.15
- 更新以支持最新填报系统（感谢 Housyou 的 contribution）
- 增加 Github Actions（感谢 ErnestDong 的 contribution）

### version 3.1

- 发布于 2021.11.6
- 更新了 Linux 的 phantomjs 版本（感谢 David Wang 的 contribution）

### version 3.0

- 发布于 2021.3.10
- 支持多人同时填报
- 修复 driver 启动时可能出现的问题（感谢 AOZMH 的 contribution）
- 优化运行稳定性

### version 2.3

- 发布于 2020.10.19
- 加入微信推送功能（感谢 XiaoTian 的 contribution）
- 支持 Linux 系统
- 修复填报逻辑问题可能引发的错误
- 终极修复【希望吧】可能的会话失效导致填报失败的问题
- 统一代码风格

### version 2.1

- 发布于 2020.10.11
- 加入 mac OS 取消定时运行
- 第一个 release 版本

### version 2.0

- 发布于 2020.10.10
- 支持 mac OS 设置定时运行，并加入运行前环境检查（感谢 mojave 的 contribution）

### version 1.9.1

- 发布于 2020.10.10
- 修复填报入校备案时可能出现的会话失效导致填报失败的问题

### version 1.9

- 发布于 2020.10.5
- 支持 mac OS 系统（感谢 JuiAnHsu 的 contribution）

### version 1.1

- 发布于 2020.10.5
- 修复 iaaa 认证时第一次必触发 500 错误的问题（感谢 Rainshaw 的 contribution）

### version 1.0

- 发布于 2020.10.4
- 项目初始版本
