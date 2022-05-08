package org.jiangze.entil;

public class Point {
    private double x;
    private double y;

    public Point(Point point) {
        this.x = point.x;
        this.y = point.y;
    }


//    因为在map中将point作为键，默认是将point的地址进行比较，所以这里需要重定义hash函数

//    @Override
//    public int hashCode() {
////        System.out.println((int)Integer.parseInt(String.valueOf((((Double)this.x).intValue()))+String.valueOf((((Double)this.x).intValue()))));
//        return (int)Integer.parseInt(String.valueOf((((Double)this.x).intValue()))+String.valueOf((((Double)this.x).intValue())));
//    }

    @Override
    public boolean equals(Object obj) {

        Point temp =(Point)obj;
        return (this.x == temp.getX()) && (this.y==temp.getY());

    }

    /**
     * 获取与另外一个点的距离
     *
     * @param point
     * @return
     */
    public double getDistance(Point point) {
        return Math.sqrt(getDistancePow(point));
    }

    public double getDistancePow(Point point) {
        return (x - point.getX()) * (x - point.getX()) + (y - point.getY()) * (y - point.getY());
    }


    public Point() {
        this.x = 0;
        this.y = 0;
    }

    public Point(double x,double y) {
        this.x = x;
        this.y = y;
    }
    @Override
    public String toString() {
        return "(" + this.x + "," + this.y + ")";
    }
    public double getX() {
        return x;
    }

    public double getY() {
        return y;
    }

    public void setX(double x) {
        this.x = x;
    }

    public void setY(double y) {
        this.y = y;
    }
}
