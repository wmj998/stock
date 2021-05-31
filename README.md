## Get real time stock price

通过URL获取web页面数据，对数据进行清洗和处理，存储在mysql中，并根据数据库中的数据进行分析和预测

### relation_mysql

MySQL数据库操作模块

### pd_mysql

pandas数据与数据库的读取、存储模块

### plot_acf

数据的自相关图模块

### ADF

数据的单位根检验模块

### plot_pacf

数据的偏自相关图模块

### acorr_ljungbox

数据的白噪声检验模块

### ARIMA

用于预测的时序模型



+ get_html() 获取网页数据
+ get_data() 处理数据
+ create_db() 创建数据库
+ save_data() 数据保存，read_data() 数据读取
+ visual() 数据可视化分析，predict() 数据预测



