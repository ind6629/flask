function clickTable(){
  var chartDom = document.querySelector('.showBox');
  var myChart = echarts.init(chartDom);
    var option;

  datax = [];
  datay = [];
  console.log(records);
  records.forEach(record => {
    datax.push(`${record.search_count}`);
    datay.push(`${record.category}`);
    //console.log(`${product.event_id},${product.interaction_count}`);
    });
  console.log(datax,datay);
    
    option = {
      yAxis: {  // 将原来的 xAxis 改为 yAxis（纵向显示分类）
        type: 'category',
        data: datay
      },
      xAxis: {  // 将原来的 yAxis 改为 xAxis（横向显示数值）
        type: 'value'
      },
      series: [
        {
          data: datax,
          type: 'bar'  // 仍然是 'bar'，但 ECharts 会根据坐标轴自动调整为横向
        }
      ]
    };
    
    option && myChart.setOption(option);
    console.log('加载');
}



document.addEventListener('DOMContentLoaded', function() {
    clickTable();
  });