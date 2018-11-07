package com.example.ttetu.podocollect.util;

import android.content.Context;
import android.util.Log;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONObject;

public class Requester {

    private RequestQueue queue;

    public Requester(Context context) {
        queue = Volley.newRequestQueue(context);
    }

    public void getRequest(String url, final GetCallBack callBack){
        // Request a string response from the provided URL.
        JsonArrayRequest jsonArrayRequest = new JsonArrayRequest
                (Request.Method.GET, url, null, new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        callBack.onSuccess(response);
                    }
                }, new Response.ErrorListener() {

                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.d("D", "onErrorResponse: no response");
                    }
                });
// Add the request to the RequestQueue.
        queue.add(jsonArrayRequest);
        queue.start();
    }

    public void postRequest(String url, JSONObject jsonObject, final PostCallBack callBack){
        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, url, jsonObject, new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                Log.d("D", "onSuccess" + response.toString());
                callBack.onSuccess(response);
            }
        }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                Log.d("D", "onErrorResponse: no response" + error.toString());
                callBack.onError(error);
            }
        });
// Add the request to the RequestQueue.
        queue.add(jsonObjectRequest);
        queue.start();
    }
}
