package org.jiangze.entil;

import java.util.ArrayList;

public class Clusters {
    private ArrayList<Point> cluster;
    private Point centroid;

    public Clusters() {
        cluster = new ArrayList<Point>();
        centroid = new Point();
    }

    public ArrayList<Point> getCluster() {
        return cluster;
    }

    public void setCentroid(Point centroid) {
        this.centroid = centroid;
    }
    public  Point getI(int i ){
        return cluster.get(i);
    }

    public Point getCentroid() {
        return centroid;
    }

    public Clusters(Point point,Point centroid) {
        cluster = new ArrayList<Point>();
        cluster.add(point);
        this.centroid = centroid;
    }
    public void addPoint(Point point) {
        cluster.add(point);
    }

    public int size() {
        return cluster.size();
    }

    /**
     * 获取一个cluster的SSE
     *
     * @param
     * @return
     */
    public double getSSEofACluster() {
        double SSEofACluster = 0;
        for (Point point : cluster) {
//            System.out.print( "centroid"+centroid+"point "+point+ "point.getDistancePow()"+point.getDistancePow(this.centroid));
            SSEofACluster += point.getDistancePow(this.centroid);

        }
//        System.out.println("centroid "+ centroid+" " +SSEofACluster);
        return SSEofACluster;
    }


    public boolean isEmpty() {
        return cluster.isEmpty();
    }

    /**
     * 显示一个簇
     */
    public void printPoint() {
//        System.out.println("centroid"+centroid);
        for (int i = 0; i < cluster.size(); i++) {
            System.out.print(cluster.get(i));
        }
        System.out.println();
    }

    /**
     * 更新一个簇的质心
     */
    public void updateCentroid(){

        double sumX = 0 ;
        double sumY = 0;
        for(Point point: cluster){
            sumX += point.getX();
            sumY+= point.getY();

        }

        double newx =(sumX/(double) cluster.size());
        double newy = (sumY/(double) cluster.size());
        setCentroid(new Point(newx,newy));
//        System.out.println("aaa"+centroid);
//        System.out.println("bbb"+cluster.get(0));
    }


}
