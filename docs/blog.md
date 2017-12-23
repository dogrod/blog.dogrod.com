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
- [ ] 发表评论接口。
- [ ] 使用用户系统的用户进行评论。
- [ ] 前台前端工程构建。
- [ ] 后台前端工程构建。

## REST APIs

#### 前台接口

**1. 获取所有Posts**

**请求URL：** /api/blog/posts

**请求类型：** GET

**请求参数列表：**

Property | Description | Type | Remark
---- | --- | --- | ---
page | 页码 | number | -
pageSize | 每页内容数量 | number | -

**响应参数列表：**

Property | Description | Type | Remark
---- | --- | --- | ---
total | post总数 | number | - 
pageNumber | 当前页码 | number | - 
pageSize | 每页post数量 | number | - 
pageCount | 总页数 | number | - 
results | Post数组 | array | -
- id | post ID | number | -
- title | 标题 | string | -
- slug | slug | string | -
- author | 作者 | object | -
-- username | 用户名 | string | -
-- email | 邮箱 | string | -
- publish_at | 发布时间 | date | -
- tags | 标签 | string | -

**2. 获取Post详情**

**请求URL：** /api/blog/post/:id

**请求类型：** GET

**请求参数列表：None**

**响应参数列表：**

Property | Description | Type | Remark
---- | --- | --- | ---
id | post ID | number | -
title | 标题 | string | -
content | 内容 | string | markdown 格式文字
slug | slug | string | -
author | 作者 | object | -
- username | 用户名 | string | -
- email | 邮箱 | string | -
publish_at | 发布时间 | date | -
comments | 评论（暂不开放） | array | -
- name | 评论人 | string | -
- create_at | 发表时间 | date | - 
- body | 评论内容 | string | -
tags | 标签 | string | 以英文逗号(,)分割

**3. 获取所有Tags**

**请求URL：** /api/blog/tags

**请求类型：** GET

**请求参数列表：None**

**响应参数列表：**

Property | Description | Type | Remark
---- | --- | --- | ---
tags | 包含所有tags的数组 | array | - 
- id | id | number | -
- name | tag名称 | string | -
-slug | tag slug | string | -

**4. 获取指定tag下的posts**

**请求URL：** /api/blog/tag/:tag_slug

**请求类型：** GET

**请求参数列表：**

Property | Description | Type | Remark
---- | --- | --- | ---
page | 页码 | number | -
pageSize | 每页内容数量 | number | -

**响应参数列表：**

Property | Description | Type | Remark
---- | --- | --- | ---
total | post总数 | number | - 
pageNumber | 当前页码 | number | - 
pageSize | 每页post数量 | number | - 
pageCount | 总页数 | number | - 
results | Post数组 | array | -
- id | post ID | number | -
- title | 标题 | string | -
- slug | slug | string | -
- author | 作者 | object | -
-- username | 用户名 | string | -
-- email | 邮箱 | string | -
- publish_at | 发布时间 | date | -
- tags | 标签 | string | -


## Models

#### Post

Property | Type | Description | Unique | Default | Migrations | Remark
--- | ---  | ---    | ---     | ---        | --- |
title | CharField | 标题 | no | - | - | -
slug | SlugField | slug | no | - | - | -
author | ForeignKey(User) | 作者 | no | - | - | -
body | TextField | 内容 | no | - | - | -
publish_at | DateTimeField | 发布时间 | no | - | - | -
create_at | DateTimeField | 创建时间 | no | - | - | -
update_at | DateTimeField | 更新时间 | no | - | - | -
status | CharField | 发布状态 | no | draft | - | - 
tags | TaggableManager | tag | no | - | - | 通过django-taggit创建

#### Comment

Property | Type | Description | Unique | Default | Migrations | Remark
--- | ---  | ---    | ---     | ---        | --- |
post | ForeignKey(Post) | 关联post | no | - | - | -
name | CharField | 评论人 | no | - | - | -
email | EmailField | email | no | - | - | -
body | TextField | 评论内容 | no | - | - | -
create_at | DateTimeField | 创建时间 | no | - | - | -
update_at | DateTimeField | 更新时间 | no | - | - | -
active | BooleanField | 是否可见 | no | True | - | -
