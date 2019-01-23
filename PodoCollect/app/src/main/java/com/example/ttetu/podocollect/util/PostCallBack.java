package com.example.ttetu.podocollect.util;

import com.android.volley.VolleyError;

import org.json.JSONObject;

public interface PostCallBack {
    void onSuccess(JSONObject jsonObject);
    void onError(VolleyError error);
}
