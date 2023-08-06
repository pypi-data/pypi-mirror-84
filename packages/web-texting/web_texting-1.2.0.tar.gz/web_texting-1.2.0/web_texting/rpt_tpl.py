class RptTemplate:

    html_template = u"""
<?xml version="1.0" encoding="UTF-8"?>
<html>
<head>
    <title>测试报告</title>
    <meta name="generator" content="HTMLTestRunner 0.8.2.2"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
    <script src="http://libs.baidu.com/jquery/2.0.0/jquery.min.js"></script>
    <script src="http://libs.baidu.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>

    <!-- 引入 echarts.js -->
    <script type="text/javascript" 
        src="http://echarts.baidu.com/gallery/vendors/echarts/echarts-all-3.js"></script>
    <script type="text/javascript" 
        src="http://echarts.baidu.com/gallery/vendors/echarts-stat/ecStat.min.js"></script>
    <script type="text/javascript" 
        src="http://echarts.baidu.com/gallery/vendors/echarts/extension/dataTool.min.js"></script>

    <style type="text/css" media="screen">
        body {
            margin: 0;
            font-family: "Arial", "Microsoft YaHei", "黑体", "宋体", sans-serif;
            font-size: 18px;
            line-height: 1.5;
            line-height: 1.5;
            color: #333333;
        }

        .table {
            margin-bottom: 1px;
            width: 100%;
        }

        .hiddenRow {
            display: none;
        }

        .container-fluid {
            padding-right: 120px;
            padding-left: 120px;
        }

        .nav-tabs li {
            width: 186px;
            text-align: center;
        }
    </style>
</head>

<body >
    <script language="javascript" type="text/javascript">

    function showClassDetail(detail_id, hiddenRow_id, class_type) {
        console.log(document.getElementById(hiddenRow_id).className)

        if ('详细' ==  document.getElementById(detail_id).innerText) {
            if ('all' == class_type) {
                document.getElementById(hiddenRow_id).className = 'all';
            }
            else if ('success' == class_type) {
                document.getElementById(hiddenRow_id).className = 'success';
            }
            else if ('error' == class_type) {
                document.getElementById(hiddenRow_id).className = 'error';
            }
            else{
                document.getElementById(hiddenRow_id).className = 'untreaded';
            }
            document.getElementById(detail_id).innerText = "收起"
        }
        else {
            document.getElementById(detail_id).innerText = "详细"
            document.getElementById(hiddenRow_id).className = 'hiddenRow';
        }
    }

    </script>

    <div class="container-fluid">
        <div class="page-header">
            <h1 class="text-primary" style="font-size:45px;line-height:75px">自动化测试报告</h1>
        </div>

        <div class="col-md-12">
            <div class="col-md-4" style="Background-Color:#F5F5F5; height:300px">
                <h3 style="line-height:25px">基本信息</h3>
                <table class="table table-hover table-bordered" style="width:100% height:11px">
                    <tbody>
                        <tr class="info">
                            <td class="text-center">开始时间</td>
                            <td class="text-center">{{start_time}}</td>
                        </tr>
                        <tr class="info">
                            <td class="text-center">结束时间</td>
                            <td class="text-center">{{end_time}}</td>
                        </tr>
                        <tr class="info">
                            <td class="text-center">测试用时</td>
                            <td class="text-center">{{used_time}}</td>
                        </tr>
                        <tr class="info">
                            <td class="text-center">总步骤数</td>
                            <td class="text-center">{{sum_all_cases}}</td>
                        </tr>
                        <tr class="info">
                            <td class="text-center">执行步骤数</td>
                            <td class="text-center">{{sum_executed_cases}}</td>
                        </tr>
                        <tr class="info">
                            <td class="text-center">跳过步骤数</td>
                            <td class="text-center">{{sum_untreaded_cases}}</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="col-md-8">
                <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
                <div id="main" style="height:300px;"></div>
                <script type="text/javascript">
                    var myChart = echarts.init(document.getElementById('main'));
                    var option = {
                    backgroundColor: '#F5F5F5', //背景色

                    title: {
                        text: '测试统计数据',
                        x: 'center'
                    },

                    legend: {
                        orient: 'vertical',
                        x: 'left',
                        data: ['成功', '失败', '未执行']
                    },

                    color: ['#3c763d', '#a94442', '#0099CC'],

                    calculable: true,

                    series: [{
                        name: '测试结果',
                        type: 'pie',
                        radius: '55%',
                        center: ['50%', '60%'],
                        startAngle: 135,
                        data: [{
                            value: {{right_sum}},
                            name: '成功',
                            itemStyle: {
                                normal: {
                                    label: {
                                        formatter: '{b} : {c} ({d}%)',
                                        textStyle: {
                                            align: 'left',
                                            fontSize: 15,
                                        }
                                    },
                                    labelLine: {
                                         length: 40,
                                    }
                                 }
                            }
                        }, {
                            value: {{error_sum}},
                            name: '失败',
                            itemStyle: {
                                normal: {
                                    label: {
                                        formatter: '{b} : {c} ({d}%)',
                                        textStyle: {
                                            align: 'right',
                                            fontSize: 15,
                                        }
                                    },
                                    labelLine: {
                                        length: 40,
                                        }
                                    }
                                }
                            }, {
                            value: {{untreated_sum}},
                            name: '未执行',
                            itemStyle: {
                                normal: {
                                    label: {
                                        formatter: '{b} : {c} ({d}%)',
                                        textStyle: {
                                            align: 'right',
                                            fontSize: 15,
                                        }
                                   },
                                    labelLine: {
                                        length: 40,
                                        }
                                   }
                               }
                           }],
                        }]
                    };
                    // 为echarts对象加载数据
                    myChart.setOption(option);
                </script>
            </div>
        </div>
    """

    report_Label = '''
    <div><span>&nbsp;</span></div>

    <div class="col-md-12">
        <div class="tabbable" id="tabs-957640">
            <ul class="nav nav-tabs">
                <li class="active">
                    <a href="#panel-0" data-toggle="tab" style="Background-Color: #428bca; color: #fff;">
                        执  行 ({})
                    </a>
                </li>
                <li>
                    <a href="#panel-1" data-toggle="tab" style="Background-Color: #d9534f; color: #fff;">
                        成  功 ({})
                    </a>
                </li>
                <li>
                    <a href="#panel-2" data-toggle="tab" style="Background-Color: #5cb85c; color: #fff;">
                        失  败 ({})
                    </a>
                </li>
                <li>
                    <a href="#panel-3" data-toggle="tab" style="Background-Color: #5bc0de; color: #fff;">
                        未执行 ({})
                    </a>
                </li>
            </ul>
        </div>
        <div class="tab-content">
            <div class="tab-pane active" id="panel-0">
                <table class="table table-hover table-bordered">
{}
                </table>
            </div>


            <div class="tab-pane" id="panel-1">
                <table class="table table-hover table-bordered">
{}
                </table>
            </div>


            <div class="tab-pane" id="panel-2">
                <table class="table table-hover table-bordered">
{}
                </table>
            </div>


            <div class="tab-pane" id="panel-3">
                <table class="table table-hover table-bordered">
{}
                </table>
            </div>
        </div>
    </div>


</div>
</body>
</html>
    '''

    report_title = '''
                <table class="table table-hover table-bordered" style="Background-Color:#dff0d8">
                    <thead>
                        <colgroup>
    {}
                        </colgroup>
                        <tr>
    {}
                        </tr>
                    </thead>
                    <tbody></tbody>
                </table>
     '''

    report_title_width = '''                         <col width='{}%'/>
    '''

    report_title_label = '''                         <td class="text-center"  style="Background-Color:#dff0d8">{}</td>
    '''

    report_table_data = '''                           <td class="text-center">{}</td>
    '''

    report_table_detail = '''                           <td class="text-center">
    <a href="javascript:showClassDetail('{}','{}', '{}')" class="detail" id = "{}">
        详细
    </a></td>
    '''

    report_detail_text = '''                   <tr class='hiddenRow' id="{}" >
                           <td colspan='{}'>
                               <div>
                                   <pre class="text-left">
    {}
                                   </pre>
                               </div>
                           </td>
                       </tr>
    '''

    pass
