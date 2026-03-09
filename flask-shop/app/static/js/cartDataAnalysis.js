function clickTable(){
    var chartDom = document.querySelector('.showBox');
    var myChart = echarts.init(chartDom);
    var option;
  
    list_data = [];
    console.log(carts);
    carts.forEach(cart => {
        item = {};
        item['name'] = `${cart.category}`;
        item['value'] = `${cart.count}`;
        list_data.push(item);
        //datax.push(`${record.search_count}`);
      });
    console.log(list_data);

    option = {
      title: {
        text: '购物车中商品分析',
        subtext: '商品类别占比',
        left: 'center'
      },
      tooltip: {
        trigger: 'item'
      },
      legend: {
        orient: 'vertical',
        left: 'left'
      },
      series: [
        {
          name: '具体数量',
          type: 'pie',
          radius: '50%',
          data: list_data,
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    };
    
    option && myChart.setOption(option);
    
      console.log('加载');
  }
  
  
  
  document.addEventListener('DOMContentLoaded', function() {
      clickTable();
    });