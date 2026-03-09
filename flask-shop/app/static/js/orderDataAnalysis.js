function clickTable(){
    //console.log(orders);
    datax = [];
    list_data = []
    orders.forEach(order => {
        datax.push(`${order.date}`);
        item = {};
        item['value'] = `${order.count}`;
        item['label'] = {show: true, formatter: `${order.category}` };
        list_data.push(item);
      });
    // console.log(datax);
    // console.log(list_data);


    var chartDom = document.querySelector('.showBox');
    var myChart = echarts.init(chartDom);
    var option;

    option = {
        xAxis: {
          type: 'category',
          data: datax
        },
        yAxis: { type: 'value' },
        series: [{
          data: list_data,
          type: 'line',
          label: {  // 默认配置
            show: true,
            position: 'top',
            color: '#333',
            fontSize: 12
          }
        }]
      };
    
    option && myChart.setOption(option);
    console.log('加载订单数据');
}
  
  
  
document.addEventListener('DOMContentLoaded', function() {
    clickTable();
});