# Blog - 不唠嗑

博客系统后端API和Model文档。

**Feature:**
- 通过Django Admin编写发布博客。
- REST API输出博文列表和博文详情。
- Django渲染Post List & Post Detail页面。（前后端分离后将移除）
- 支持跨域（CORS）。
- tag功能（通过dajngo-taggit实现）。
- 评论功能（暂未开放）。

**TO-DO**
- [ ] REST API输出tag列表以及tag详情。
- [ ] 接入用户系统。
- [ ] 使用用户系统的用户进行评论。
- [ ] 前端工程构建。

## REST APIs

#### 前台接口

**1. 获取所有Posts**

**请求URL：** /api/posts

**请求类型：** GET

**请求参数列表：**

name | meaning | type | remark
---- | --- | --- | ---
page | 页码 | number |

**响应参数列表：**

name | meaning | type | remark
---- | --- | --- | ---
    | 根数组 | array |
- id | post ID | number |
- title | 标题 | string |
- slug | slug | string |
- author | 作者 | string |
- publish_at | 发布时间 | date |
- tags | 标签 | string |

**2. 获取Post详情**

**请求URL：** /api/post/:id

**请求类型：** GET

**请求参数列表：None**

**响应参数列表：**

name | meaning | type | remark
---- | --- | --- | ---
id | post ID | number |
title | 标题 | string |
slug | slug | string |
author | 作者 | string |
publish_at | 发布时间 | date |
comments | 评论（暂不开放） | array |
- name | 评论人 | string | 
- create_at | 发表时间 | date | 
- body | 评论内容 | string | 
tags | 标签 | string | 以英文逗号(,)分割

## Models

#### Post

文档正在完善...

Docs are under construction...

#### Comment

文档正在完善...

Docs are under construction...