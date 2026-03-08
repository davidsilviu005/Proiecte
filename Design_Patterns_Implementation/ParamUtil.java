package org.example;

import java.util.Map;

public class ParamUtil {
    public ParamUtil() {}

    public static String get(Map<String, String> params, String... keys) {
        for (String k : keys) {
            if (k == null) continue;
            String v = params.get(k);
            if (v == null) continue;
            if (!v.isEmpty()) return v;
        }
        return "";
    }

    public static Integer getInt(Map<String, String> params, String... keys) {
        String s = get(params, keys);
        try {
            return Integer.parseInt(s);
        } catch (NumberFormatException e) {
            return null;
        }
    }

    public static Double getDouble(Map<String, String> params, String... keys) {
        String s = get(params, keys);
        try {
            return Double.parseDouble(s);
        } catch (NumberFormatException e) {
            return null;
        }
    }
}
