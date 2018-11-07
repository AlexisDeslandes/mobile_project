package com.example.ttetu.podocollect.util;

import com.android.volley.VolleyError;

import org.json.JSONArray;

public interface GetCallBack {
    void onSuccess(JSONArray result);
    void onError(VolleyError error);
}
