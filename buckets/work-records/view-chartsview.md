
| 普通 | AI Prompt  |
| ---- | ---------- |
| 进阶 | Rules、MCP |
| 高级 |            |

## WordCloud

```chartsview
#-----------------#
#- chart type    -#
#-----------------#
type: WordCloud

#-----------------#
#- chart data    -#
#-----------------#
data: "wordcount:/"

#-----------------#
#- chart options -#
#-----------------#
options:
  wordField: "word"
  weightField: "count"
  colorField: "count"
  wordStyle:
    rotation: 30
```

## Radar

```chartsview
#-----------------#
#- chart type    -#
#-----------------#
type: Radar

#-----------------#
#- chart data    -#
#-----------------#
data:
  - item: "Design"
    user: "a"
    score: 70
  - item: "Design"
    user: "b"
    score: 30
  - item: "Marketing"
    user: "a"
    score: 50
  - item: "Marketing"
    user: "b"
    score: 60
  - item: "Technology"
    user: "a"
    score: 50
  - item: "Technology"
    user: "b"
    score: 40
  - item: "Support"
    user: "a"
    score: 30
  - item: "Support"
    user: "b"
    score: 40
  - item: "Sales"
    user: "a"
    score: 60
  - item: "Sales"
    user: "b"
    score: 40

#-----------------#
#- chart options -#
#-----------------#
options:
  xField: "item"
  yField: "score"
  seriesField: "user"
  meta:
    score:
      alias: "Score"
      min: 0
      nice: true
  xAxis:
    line: null
    tickLine: null
  yAxis:
    label: false
    grid:
      alternateColor: "rgba(0, 0, 0, 0.04)"
  point: {}
  area: {}
```

```chartsview
#-----------------#
#- chart type    -#
#-----------------#
type: Radar

#-----------------#
#- chart data    -#
#-----------------#
data:
  - item: "输入控制力（Input Control）"
    user: "a"
    score: 5
  - item: "输出可控性（Output Control）"
    user: "a"
    score: 5
  - item: "任务建模力（Task Modeling）"
    user: "a"
    score: 5
  - item: "风险与约束意识（Risk Control）"
    user: "a"
    score: 5
  - item: "系统与流程设计力（System Design）"
    user: "a"
    score: 5

#-----------------#
#- chart options -#
#-----------------#
options:
  xField: "item"
  yField: "score"
  seriesField: "user"
  meta:
    score:
      alias: "Score"
      min: 0
      nice: true
  xAxis:
    line: null
    tickLine: null
  yAxis:
    label: false
    grid:
      alternateColor: "rgba(0, 0, 0, 0.04)"
  point: {}
  area: {}
```


|**总分区间**|**等级标签**|**精确定义**|
|---|---|---|
|0–7|结果依赖型|完全黑箱使用|
|8–12|表达控制型|可控输出，但不可复现|
|13–17|任务建模型|稳定流程能力|
|18–22|系统约束型|可上线系统|
|23–25|结构重构型|可改组织|

## WordCloud

```chartsview
#-----------------#
#- chart type    -#
#-----------------#
type: WordCloud

#-----------------#
#- chart data    -#
#-----------------#
data:
  - x: "China"
    value: 2383220000
    category: "asia"
  - x: "Indonesia"
    value: 263510000
    category: "asia"
  - x: "Pakistan"
    value: 396459000
    category: "asia"
  - x: "Russia"
    value: 546804372
    category: "europe"
  - x: "Japan"
    value: 126790000
    category: "asia"
  - x: "Vietnam"
    value: 92700000
    category: "asia"
  - x: "Germany"
    value: 82800000
    category: "europe"
  - x: "Iran"
    value: 80135400
    category: "asia"
  - x: "Thailand"
    value: 68298000
    category: "asia"
  - x: "France"
    value: 67013000
    category: "europe"
  - x: "Italy"
    value: 60599936
    category: "europe"
  - x: "South Korea"
    value: 51446201
    category: "asia"
  - x: "Kenya"
    value: 48467000
    category: "africa"
  - x: "Spain"
    value: 46812000
    category: "europe"
  - x: "Sudan"
    value: 42176000
    category: "africa"
  - x: "Iraq"
    value: 47883543
    category: "asia"
  - x: "Nepal"
    value: 28825709
    category: "asia"
  - x: "North Korea"
    value: 24213510
    category: "asia"
  - x: "Chile"
    value: 28191900
    category: "america"

#-----------------#
#- chart options -#
#-----------------#
options:
  wordField: "x"
  weightField: "value"
  color: "#122c6a"
  wordStyle:
    fontFamily: "Verdana"
    fontSize: [24, 80]
  interactions:
    type: "element-active"
  style:
    backgroundColor: "white"
  state:
    active:
      style:
        lineWidth: 3
```

```chartsview
#-----------------#
#- chart type    -#
#-----------------#
type: WordCloud

#-----------------#
#- chart data    -#
#-----------------#
data: |
  dataviewjs:
  return dv.pages()
           .flatMap(p => p.file.etags)
           .groupBy(p => p)
           .map(p => ({tag: p.key, count: p.rows.length}))
           .array();

#-----------------#
#- chart options -#
#-----------------#
options:
  wordField: "tag"
  weightField: "count"
  colorField: "count"
  wordStyle:
    rotation: 30
  enableSearchInteraction:
    operator: tag
```

## 相关笔记

- [[buckets/work-records/view-flowchart]] — Mermaid 流程图（同为可视化工具）