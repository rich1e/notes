## 功能

- 支持 `json` 数据动态生成
- 支持多个自定义组件

## 数据格式

**Uniseriate / Biserial**

```js
const formConfig: ConfigType = {
  scene: 'uniseriate',
  field: [
    // ...
    {
      control: 'Slots',
      label: '自定义1',
      prop: 'slots1',
    },
    {
      control: 'Slots',
      label: '自定义2',
      prop: 'slots2',
    }
  ],
  // ...
};
```
**Group**

```js
const formConfig: ConfigType = {
  scene: 'group',
  groups: [
    [
      {
        control: 'Slots',
        label: '自定义1',
        prop: 'slots1',
      },
    ],
    [
      {
        control: 'Slots',
        label: '自定义2',
        prop: 'slots2',
      }
    ],
  ]
  // ...
};
```
**Tab**

```js
const formConfig: ConfigType = {
  scene: 'tab',
  tabs: {
    tabType: 'border-card',
    tabPanes: [
      {
        title: 'Uniseriate',
        paneType: 'uniseriate',
        uniseriate: [
          {
            control: 'Slots',
            label: '自定义1',
            prop: 'slots1',
          },
          {
            control: 'Slots',
            label: '自定义2',
            prop: 'slots2',
          },
        ],
      },
      {
        title: 'Biserial',
        paneType: 'biserial',
        biserial: [
          {
            control: 'Slots',
            label: '自定义3',
            prop: 'slots3',
          },
        ],
      },
      {
        title: 'Group',
        paneType: 'group',
        group: [
          [
            {
              control: 'Slots',
              label: '自定义6',
              prop: 'slots6',
            },
            {
              control: 'Slots',
              label: '自定义4',
              prop: 'slots4',
            },
          ],
          [
            {
              control: 'Slots',
              label: '自定义5',
              prop: 'slots5',
            },
          ],
        ],
      },
    ],
  },
  // ...
};
```

## 自定义组件

```html
<DynamicForm :config="formConfig">
  <template #slots1="{ fieldModel }">
    <ElInput v-model="fieldModel[`slots1`]" />
  </template>
  <template #slots2="{ fieldModel }">
    <ElInput v-model="fieldModel[`slots2`]" />
  </template>
  <template #slots3="{ fieldModel }">
    <ElInput v-model="fieldModel[`slots3`]" />
  </template>
</DynamicForm>
```

## 项目应用

![[assets/buckets/work-experience/max-optics/Attr - 动态表单Slots设计/IMG-20260403174656813.png]]

![[assets/buckets/work-experience/max-optics/Attr - 动态表单Slots设计/IMG-20260403174656845.png]]

## 优化对比

- HTML 结构优化
- Style Code 减少，没有复杂的样式计算
- UI 模板灵活扩展，可重复使用
- Typescript 类型定义清晰，结合IDE提示属性字段类型，减少编码时错误

![[assets/buckets/work-experience/max-optics/Attr - 动态表单Slots设计/IMG-20260403174656862.png]]

![[assets/buckets/work-experience/max-optics/Attr - 动态表单Slots设计/IMG-20260403174656883.png]]

![[assets/buckets/work-experience/max-optics/Attr - 动态表单Slots设计/IMG-20260403174656903.png]]

![[assets/buckets/work-experience/max-optics/Attr - 动态表单Slots设计/IMG-20260403174656931.png]]

![[assets/buckets/work-experience/max-optics/Attr - 动态表单Slots设计/IMG-20260403174656949.png]]

![[assets/buckets/work-experience/max-optics/Attr - 动态表单Slots设计/IMG-20260403174656969.png]]

## npm 

![[assets/buckets/work-experience/max-optics/Attr - 动态表单Slots设计/IMG-20260403174656986.png]]