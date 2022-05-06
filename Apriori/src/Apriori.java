import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;
import java.util.Map;

public class Apriori {

    /**
     * DB，交易事务数据库
     */
    private static List<String[]> DB = new ArrayList<String[]>();
    private static double min_confidence;
    private static double min_support;
    private static int transcation_num;
    private static Map<ArrayList<String>, ArrayList<String>> rule = new HashMap<ArrayList<String>, ArrayList<String>>();
    /**
     * Fk频繁集
     */
    private static List<Map<String, Integer>> FkList = new ArrayList<Map<String, Integer>>();

    /**
     * 读取文件
     *
     * @param input_test_file
     */
    public void read_file(String input_test_file) {
        try {
            BufferedReader br = new BufferedReader(new FileReader(new File(input_test_file)));
            String line = "";
            line = br.readLine();
            min_support = Double.valueOf(line.substring(0, line.indexOf(" ")));
            min_confidence = Double.valueOf(line.substring(line.indexOf(" ") + 1, line.length()));

            while (!(line = br.readLine()).equals("--END--")) {
                DB.add(line.split(" "));
            }
            br.close();
            System.out.println("Input para==================================");
            System.out.println("min_support  " + min_support);
            System.out.println("min_confidence   " + min_confidence);
            transcation_num = DB.size();
            System.out.println("transcation_num " + transcation_num);
            System.out.println("transcation:==============================");
            for (String[] T : DB) {
                for (String item : T)
                    System.out.print(item + "  ");
                System.out.println();
            }
            System.out.println("========================================");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * 频繁集的生成
     */

    public void frequentSet_gen() {
        //        首先生成L1
        FkList.add(get_F1());
        int k = 1;
        while (FkList.get(k - 1).size() != 0) {
            Map<String, Integer> Ck = get_Ck_from_preFk(k);
//           获取DB中的k项子集
//           计数Ck
            for (String[] transcation : DB) {
//                find ck in transcation
                Set<String> Ct = subset(Ck, transcation);
//                count Ck
                for (String item : Ct) {
                    Ck.put(item, Ck.get(item) + 1);
                }
            }
            FkList.add(filter_Ck2Fk(Ck));
            k++;
        }
    }


    /**
     * 获得F1
     *
     * @return
     */
    private Map<String, Integer> get_F1() {
        Map<String, Integer> C1 = new HashMap<String, Integer>();
        for (String[] Transcation : DB) {
            if (Transcation.length > 1) {
                for (int i = 0; i < Transcation.length; i++) {
                    if (C1.containsKey(Transcation[i])) {
                        C1.put(Transcation[i],
                                C1.get(Transcation[i]) + 1);
                    } else {
                        C1.put(Transcation[i], 1);
                    }
                }
            }
        }
        Map<String, Integer> F1 = filter_Ck2Fk(C1);
        return F1;
    }


    /**
     * Ck2Fk
     *
     * @param Ck
     * @return
     */
    private Map<String, Integer> filter_Ck2Fk(Map<String, Integer> Ck) {

        Iterator<Map.Entry<String, Integer>> iter = Ck.entrySet().iterator();
        List<String> LkList = new ArrayList<String>();
        Map<String, Integer> Fk = new HashMap<String, Integer>();
        while (iter.hasNext()) {
            Map.Entry<String, Integer> entry = iter.next();
            if (entry.getValue() >= min_support * transcation_num) {
                LkList.add(entry.getKey());
            }
        }
        for (String str : LkList) {
            Fk.put(str, Ck.get(str));
        }
        return Fk;
    }


    private void printFreItemSets() {
        System.out.println("Frequent ItemSets===============================");
        for (Map<String, Integer> map : FkList) {
            Iterator<Map.Entry<String, Integer>> iter = map.entrySet().iterator();

            while (iter.hasNext()) {
                Map.Entry<String, Integer> entry = iter.next();
                String key = entry.getKey();
                int count = entry.getValue();
                System.out.println(key + " : " + count);
            }
        }
        System.out.println("=========================================");
        System.out.println();
    }


    public boolean isAttachable(List<String> l1, List<String> l2) {
        boolean flag = true;

        if (l1 == null || l2 == null || l1.size() != l2.size()) {
            flag = false;
        } else if (l1.get(l1.size() - 1).compareTo(l2.get(l2.size() - 1)) >= 0) {
            flag = false;
        } else {
            for (int i = 0; i < l1.size() - 1; i++) {
                if (l1.get(i).equals(l2.get(i))) {
                    flag = false;
                    break;
                }
            }
        }

        return flag;
    }

    private List<String> sortStrArray(String str) {
        String[] strArray = str.split(" ");

        List<String> strList = new ArrayList<String>(Arrays.asList(strArray));
        Collections.sort(strList);

        return strList;
    }

    private boolean isHasInfrequentSubset(List<String> c, int k) {
        boolean flag = false;
        if (c != null && FkList.get(k - 1) != null) {
            List<String> subSet = null;
//            每次从中去掉一个元素，而后比较集合是否能够在Fk-1中找到
            for (int i = 0; i < c.size(); i++) {
                subSet = new ArrayList<String>(c);
                subSet.remove(i);
                String subSetStr = strList2Str(subSet);
                if (!FkList.get(k - 1).containsKey(subSetStr)) {
                    flag = true;
                    break;
                }
            }
        }

        return flag;
    }

    private String strList2Str(List<String> list) {
        String str = "";

        for (int i = 0; i < list.size() - 1; i++) {
            str += list.get(i) + " ";
        }

        str += list.get(list.size() - 1);
        return str;
    }


    private Map<String, Integer> get_Ck_from_preFk(int k) {
        List<String> pre_Fk_list = new ArrayList<String>(FkList.get(k - 1).keySet());
        Map<String, Integer> Ck = new HashMap<String, Integer>();

        for (int i = 0; i < pre_Fk_list.size(); i++) {
            for (int j = 0; j < pre_Fk_list.size(); j++) {
                List<String> l1List = sortStrArray(pre_Fk_list.get(i));
                List<String> l2List = sortStrArray(pre_Fk_list.get(j));
                List<String> c = null;
                if (isAttachable(l1List, l2List)) {
                    c = new ArrayList<String>(l1List);
                    c.add(l2List.get(l2List.size() - 1));

                    // 判断生成的项集的所有子集是否都在Lk-1中，进行剪枝操作
                    if (!isHasInfrequentSubset(c, k)) {
                        String strKey = strList2Str(c);
                        Ck.put(strKey, 0);
                    }
                }

            }
        }
        return Ck;
    }


    private Set<String> subset(Map<String, Integer> ck, String[] transcation) {
        Set<String> ct = new HashSet<String>();
        List<String> tList = Arrays.asList(transcation);

        Iterator<Map.Entry<String, Integer>> iter = ck.entrySet().iterator();

        while (iter.hasNext()) {
            Map.Entry<String, Integer> entry = iter.next();
            String key = entry.getKey();

            // 判断是否Ck中的项是否是transcation的子集，是则添加到Ct中
            if (isSubset(key.split(" "), tList)) {
                ct.add(key);
            }
        }

        return ct;
    }


    private boolean isSubset(String[] ckItem, List<String> transcation) {
        boolean flag = true;
        for (int i = 0; i < ckItem.length; i++) {
            if (!transcation.contains(ckItem[i])) {
                flag = false;
                break;
            }
        }

        return flag;
    }


    public void apriori() {
//        1，读取事务数据库，获取各种阈值
        read_file("test.txt");
//        若更改位置，请修改对应输入路径
//        2.生成频繁集
        frequentSet_gen();
        printFreItemSets();

        rule_gen();
        printf_rule();

    }

    private void rule_gen() {
//        对于每一个大于二的频繁集，首先生成频繁集的所有子集
        for (Map<String, Integer> frequentItemSets : FkList) {
            Iterator<Map.Entry<String, Integer>> iter = frequentItemSets.entrySet().iterator();
            while (iter.hasNext()) {
                Map.Entry<String, Integer> entry = iter.next();
                if (entry.getKey().length() <= 1)
//                    对于频繁集F1不做处理
                    continue;
                String frequentItem = entry.getKey();
//                生成frequentItem的所有子集，而后对于每一个子集，生成规则的置信度
                ArrayList<ArrayList<String>> subSets = get_all_subSet(frequentItem.split(" "));
                for (ArrayList<String> subSet : subSets) {
                    if (isRule(subSet, frequentItem)) {

                        rule.put(subSet, get_remain_subSet(subSet, frequentItem.split(" ")));
                    }
                }
            }
        }
    }

    private void printf_rule() {
        System.out.println("Rule:****************************************");
        Iterator<Map.Entry<ArrayList<String>, ArrayList<String>>> it = rule.entrySet().iterator();
        while (it.hasNext()) {
            Map.Entry<ArrayList<String>, ArrayList<String>> entry = it.next();
            System.out.println(entry.getKey() + "-->" + get_remain_subSet(entry.getKey(), strList2Str(entry.getValue()).split(" ")));
        }
        System.out.println("******************************************");
    }


    /**
     * 获得一个集合的补集
     *
     * @param subSet
     * @param s
     * @return
     */
    private ArrayList<String> get_remain_subSet(ArrayList<String> subSet, String[] s) {
        boolean[] exsit = new boolean[s.length];
        for(boolean a:exsit){
            a=false;
        }
        for (String strSub : subSet) {
            for (int i = 0; i < s.length; i++) {
//                System.out.println(strSub+"  ==  "+s[i]);
                if (strSub.equals(s[i])) {
                    exsit[i] = true;
                }
            }
        }
        ArrayList<String> remain_subSet = new ArrayList<String>();
        for (int i = 0; i < s.length; i++) {
            if (!exsit[i]) {
                remain_subSet.add(s[i]);
            }
        }
        return remain_subSet;
    }

    /**
     * 判断一个规则的置信度是否大于最小置信度
     *
     * @param subSet
     * @param frequentItem
     * @return
     */


//    及其可能出现BUG！！！！
    private boolean isRule(ArrayList<String> subSet, String frequentItem) {
//        计算置信度 S(frequentItem)/S(subSet)
        if (subSet.size() == frequentItem.split(" ").length || subSet.size() == 0)
            return false;


        Map<String, Integer> map_subSet = new HashMap<String, Integer>();
        map_subSet.put(strList2Str(subSet), 0);

        for (String[] transcation : DB) {
            if (isSubset(strList2Str(subSet).split(" "), Arrays.asList(transcation.clone()))) {
                map_subSet.put(strList2Str(subSet), map_subSet.get(strList2Str(subSet)) + 1);
            }
        }
//
        Map<String, Integer> map_frequent = new HashMap<String, Integer>();
        map_frequent.put(frequentItem, 0);
        for (String[] transcation : DB) {
            if (isSubset(frequentItem.split(" "), Arrays.asList(transcation.clone()))) {
                map_frequent.put(frequentItem, map_frequent.get(frequentItem) + 1);
            }
        }

        double conf = (map_subSet.get(strList2Str(subSet))) / (map_frequent.get(frequentItem));
        if (conf >= min_confidence)
            return true;
        return false;

    }


    /**
     * 生成S的所有子集
     *
     * @param s
     * @return
     */
    private ArrayList<ArrayList<String>> get_all_subSet(String[] s) {
        Arrays.sort(s);//正序排序，保证按照字典顺序排序
        ArrayList<ArrayList<String>> subSets = new ArrayList<ArrayList<String>>();
        int n = s.length;
        int sum = 1;
        for (int i = 0; i < n; i++) {
            sum = sum * 2;
        }
        for (int i = sum - 1; i >= 0; i--) {
            ArrayList a = new ArrayList();
            for (int j = n - 1; j >= 0; j--) {
                if (((i >> j) & 1) == 1) {//判断j位上是否为1,从高位开始检查
                    a.add(s[j]);
                }
            }
            subSets.add(a);
        }
        return subSets;
    }


    public static void main(String[] args) {

        new Apriori().apriori();
    }
}
