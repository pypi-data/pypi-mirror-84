import os
import webbrowser

class Bchart():
        #CharttJs Intialial HTML Tag
        __ChartjsCDN = '''https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0-rc.1/Chart.bundle.js'''
        __ScriptTag = '''<script src="{}">
                     </script>'''.format(__ChartjsCDN)
        __ChartjsStyle = '''<div class="container" style= "width:600px;height:600px;">'''
        __ChartjsTag = '''<canvas id="examChart"></canvas></div>'''
        __ChartJSIni = __ScriptTag + __ChartjsStyle+ __ChartjsTag
       #ChartJs JavaScript Strings
        __Chartjs_JScript_a = '''<script type="text/javascript">
                     var ctx = document.getElementById("examChart").getContext("2d");
                     var myChart = new Chart(ctx, {'''
        __ChartType_JScript_b =  '''type: 'bar','''
        __ChartData_JScript_c = '''data: { labels:'''
        __ChartLable_JScript_d = '[0,0,0],'
        __ChartDataSet_JScript_e = '''datasets: [{ label: 'Demo','''
        __ChartDataSetData_JScript_f = '''data:[0,0,0],'''
        __ChartDataBackground_JScript_g =  '''backgroundColor: [],'''
        __ChartDataBorder_JScript_h =  '''borderColor: [],'''
        __ChartRemain_JScript_i =  '''borderWidth: 1
               }]
              },
        options: {
        scales: {
        xAxes: [{  
         } ] } } } );</script>'''


        def chart_style_conf(self,width=None,hieght=None):
            self.__ChartjsStyle = '''width:{}px;height:{}px;">'''.format(width,hieght)

        def chart_data(self,ctype='bar',xdata=None,ydata=None):
            self.__ChartType_JScript_b =  '''type: '{}','''.format(ctype)
            self.__ChartLable_JScript_d = '''['''
            for i in xdata:
                self.__ChartLable_JScript_d+=str(i)
                self.__ChartLable_JScript_d+=''','''
            self.__ChartLable_JScript_d += '''],'''

            self.__ChartDataSetData_JScript_f = '''data: ['''
            for i in ydata:
                self.__ChartDataSetData_JScript_f += str(i)
                self.__ChartDataSetData_JScript_f += ''','''
            self.__ChartDataSetData_JScript_f += '''],'''
        def project_djangoview(self):
            __output = (self.__ChartJSIni + self.__Chartjs_JScript_a + self.__ChartType_JScript_b+
                      self.__ChartData_JScript_c+self.__ChartLable_JScript_d+
                      self.__ChartDataSet_JScript_e+self.__ChartDataSetData_JScript_f+
                      self.__ChartDataBackground_JScript_g+self.__ChartDataBorder_JScript_h+
                      self.__ChartRemain_JScript_i )
            return {'chart_as':__output}
        def project_web(self):
            data = self.project_djangoview()
            html = data['chart_as']
            path = os.path.abspath('temp.html')
            url = 'file://' + path
            with open(path, 'w') as f:
                f.write(html)
            webbrowser.open(url)

        def Help(self):
            Chart = '''
        Supported Types Of Charts:
        bar, horizontalBar, line, doughnut, pie, polarArea, bubble, radar
        ChartJs Version : 2.8
        '''
            return Chart

