package org.jiangze.utils;

import org.jiangze.entil.Point;
import org.jiangze.entil.Clusters;

import java.io.*;
import java.util.ArrayList;

public class MyTool {

    static int K;

    public static int getK() {
        return K;
    }

    /**
     * 读取文件
     *
     * @param input_test_file
     */
    static public ArrayList<Clusters> read_file(String input_test_file) {

        ArrayList<Clusters> allPoint = new ArrayList<Clusters>();
        int i = 1;
        Clusters clusters = new Clusters();
        try {
            BufferedReader br = new BufferedReader(new FileReader(new File(input_test_file)));
            String line = "";
            line = br.readLine();
            K = Integer.parseInt(line);
            while (!(line = br.readLine()).equals("--END--")) {

                Point point = new Point();
                point.setX(Double.valueOf(line.split(",")[0]));
                point.setY(Double.valueOf(line.split(",")[1]));
                if (i <= K - 1) {
                    allPoint.add(new Clusters(point, point));
                    i++;
                } else {
                    clusters.addPoint(point);
                }
            }
            clusters.setCentroid(clusters.getI(0));
            allPoint.add(clusters);
            br.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return allPoint;
    }
}
