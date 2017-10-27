# CFL算法

+ 论文《Decentralized constraint satisfaction》中所提及算法的一种Python实现。（https://arxiv.org/pdf/1103.3240.pdf）

+ 本代码模拟了把CFL算法应用到路由器信道选择中的场景。代码语言Python3，需要安装Python库pygame。由于pygame和mac系统的兼容性问题，该代码在mac系统下无法正常运行。但在Ubuntu 16.04和win7系统下均能正常运行。

+ 进入cfl-routers-demo文件夹下（当前文件夹），执行python ui.py即可执行程序。

  + 程序中黑色的圆点代表路由器，路由器周围的圆代表该路由器的通信范围，圆的不同颜色代表不同的信道。

  + 鼠标左键可用于拖拽路由器的位置，按下鼠标中键可用于增加路由器，按下鼠标右键可用于删除光标所指的路由器。按Enter键执行一次CFL算法。

  + 配置文件在data文件夹下。可以在interfere_ranges.txt文件中设置不同信道的个数及其通信范围；在locations.txt文件设置路由器的个数及其初始位置；在parameters.txt文件中设置参数a和b的取值。
