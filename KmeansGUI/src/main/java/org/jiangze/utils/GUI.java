package org.jiangze.utils;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.category.CategoryDataset;
import org.jfree.data.xy.XYSeriesCollection;

import javax.swing.*;
import java.io.IOException;


public class GUI {

    private JFrame frame;

    public static void init(XYSeriesCollection dataset1, CategoryDataset dataset2){
        //创建一个主窗口来显示面板
        JFrame frame = new JFrame("Kmeans");
        frame.setLocation(10, 0);
        frame.setSize(900, 800);
        //实现简单的散点图，设置基本的数据
        JFreeChart scatterChart = ChartFactory.createScatterPlot(
                "聚类结果",// 图表标题
                "X",
                "Y",
                dataset1,//数据集，即要显示在图表上的数据
                PlotOrientation.VERTICAL,//设置方向
                true,//是否显示图例
                false,//是否显示提示
                true//是否生成URL连接
        );
        //以面板显示
        ChartPanel chartPanel = new ChartPanel(scatterChart);
        chartPanel.setPreferredSize(new java.awt.Dimension(500, 400));

        JFreeChart lineChart = ChartFactory.createLineChart(
                "SEE迭代变化",//图名字
                "迭代次数",//横坐标
                "SSE值",//纵坐标
                dataset2,//数据集
                PlotOrientation.VERTICAL,
                true, // 显示图例
                true, // 采用标准生成器
                false);// 是否生成超链接
        ChartPanel lineChartPanel = new ChartPanel(lineChart);
        lineChartPanel.setPreferredSize(new java.awt.Dimension(500, 400));
        lineChartPanel.setLocation(30,450);


        JPanel jPanel = new JPanel();
        jPanel.add(chartPanel);
        jPanel.add(lineChartPanel);
        //将主窗口的内容面板设置为图表面板
        frame.setContentPane(jPanel);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
    }

}
