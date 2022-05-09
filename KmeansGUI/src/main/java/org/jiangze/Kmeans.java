package org.jiangze;

import org.jiangze.entil.Clusters;
import org.jiangze.entil.Point;
import org.jiangze.utils.GUI;
import org.jiangze.utils.MyTool;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

public class Kmeans {
    private static int K = 0;
    private static ArrayList<Clusters> allPoints = null;
    private static ArrayList<Double> SSEList = new ArrayList<>();

    public static void main(String[] args) {
        bootKmeans();
    }
    public static void init() {
        allPoints = MyTool.read_file("src/main/resources/test.txt");
        K = MyTool.getK();
    }
    private static void bootKmeans() {
        init();
        double preSSE = 0;
        double currentSEE = getSSE();
        while(preSSE!=currentSEE  ){
            SSEList.add(currentSEE);

//            更新每一轮的质心
            updateCentroids();

//            根据计算的质心移动簇见的元素
            updateClusters();

//            更新SSE
            preSSE = currentSEE;
            currentSEE=getSSE();
        }
//        可视化展现
        showAllpoints();
        GUI.init(MyTool.getDataSet(allPoints),MyTool.getDataset(SSEList));
    }

    private static void showAllpoints() {
        int i = 1;
        for (Clusters clusters1 : allPoints) {
            System.out.print("cluster" + String.valueOf(i) + ": ");
            i++;
            clusters1.printPoint();
        }

    }

    private static void updateClusters() {
//        为了便于更新，定义一个map来理清楚簇与对应质心的关系
        Map<Point, Clusters> clustersMap = new HashMap<>();
        ArrayList<Point> cendroids = new ArrayList<>();
        for (Clusters clusters : allPoints) {
            cendroids.add(clusters.getCentroid());
        }
        for (Clusters clusters : allPoints) {
//            clusters.printPoint();
            int clusterSize = clusters.size();
            for (int i = 0; i < clusterSize; i++) {
//                难点：对于每个簇中的每个点，计算点与质心的距离，并记录最小距离，
//                而后将点从本簇中移除，加入到另外一个最近质心所在的簇中；
//                如果加入到另外一个簇中不做标记的话，下次遍历这个簇的时候会被再次计算，形成死循环,
//                或者是将这些所有的簇移入到另外临时簇中，临时簇的个数不会大于K，占用的空间一直为点的个数。
                int min_flag = 0;
                double minDistance = 999999999;
                for (int j = 0; j < cendroids.size(); j++) {
                    double tempDistance = clusters.getI(i).getDistance(cendroids.get(j));
                    if (tempDistance < minDistance) {
                        min_flag = j;
                        minDistance = tempDistance;
                    }
                }
//                如果当前质心的簇没有形成，形成一个簇，添加进去
                Point tempCentroid = cendroids.get(min_flag);
                if (!clustersMap.containsKey(tempCentroid)) {
                    clustersMap.put(tempCentroid, new Clusters(clusters.getI(i), tempCentroid));
                } else {
                    Clusters temp = clustersMap.get(tempCentroid);
                    temp.addPoint(clusters.getI(i));
                    clustersMap.put(tempCentroid, temp);
                }
            }
        }
        allPoints.clear();
        Iterator<Map.Entry<Point, Clusters>> it = clustersMap.entrySet().iterator();

        while (it.hasNext()) {
            Map.Entry entry = it.next();

            allPoints.add((Clusters) entry.getValue());
        }
    }
    private static void updateCentroids() {
        for (Clusters clusters : allPoints) {
            clusters.updateCentroid();
        }
    }
    private static double getSSE() {
        double SEE = 0;
        for (Clusters clusters : allPoints) {
            SEE += clusters.getSSEofACluster();
        }
        return SEE;
    }
}
