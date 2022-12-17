function Revenue(labels, data1, data2) {
   const ctx = document.getElementById('Revenue');
   new Chart(ctx, {
       type: 'bar',
       data: {
         labels: labels,
         datasets:
         [
             {
               label: 'Doanh thu',
               data: data1,
               backgroundColor: "blue",
               borderWidth: 1,
               order: 0
             },
             {
               label: 'Số lượt bay',
               data: data2,
               backgroundColor: "green",
               borderWidth: 1,
               type: 'line',
               order: 1
             }
         ]
       },

       options: {
         scales: {
           y: {
             beginAtZero: true
           }
         }
       }
   });
}

