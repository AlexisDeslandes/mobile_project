package com.example.ttetu.podocollect.activities;

import android.annotation.SuppressLint;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.PorterDuff;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ListView;

import com.android.volley.VolleyError;
import com.example.ttetu.podocollect.R;
import com.example.ttetu.podocollect.adapters.CoupleListAdapter;
import com.example.ttetu.podocollect.models.ArticleCouple;
import com.example.ttetu.podocollect.util.Requester;
import com.example.ttetu.podocollect.util.ServerCallBack;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

@SuppressLint("Registered")
public class EndedCollectActivity extends AppCompatActivity {

    JSONArray stepJsonArray;
    JSONArray stringJsonArray;
    CoupleListAdapter mAdapter;
    ArrayList<ArticleCouple> couples;
    ListView couplesView;
    Requester r;

    @Override
    public void onBackPressed() {
    }


    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.setContentView(R.layout.activity_ended_collect);
        couplesView = findViewById(R.id.collect_list);
        try {
            stepJsonArray = new JSONArray((String) getIntent().getSerializableExtra("stepJsonArray"));
            stringJsonArray = new JSONArray((String) getIntent().getSerializableExtra("stringJsonArray"));
            Log.i("i", "JSONARRAY: " + stepJsonArray.toString());
        } catch (JSONException e) {
            e.printStackTrace();
        }
        couples = new ArrayList<>();
        for (int i = 0; i < stringJsonArray.length(); i++){
            try {
                JSONObject o = stringJsonArray.getJSONObject(i);
                ArticleCouple c = new ArticleCouple(o.getString("startId"),o.getString("endId"),o.getInt("distance"));
                couples.add(c);
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
        mAdapter = new CoupleListAdapter(this,couples);
        couplesView.setAdapter(mAdapter);
        r = new Requester(this);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case R.id.action_send_collect:
                AlertDialog dialog = new AlertDialog.Builder(this)
                        .setTitle("Envoyer la collecte")
                        .setMessage("Etes vous sur de vouloir envoyer la collecte ?")
                        .setPositiveButton("Oui", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                //Do Something (Send + Go Back to menu)
                                r.postRequest("https://renaudcosta.pythonanywhere.com/distances", stepJsonArray, new ServerCallBack() {
                                    @Override
                                    public void onSuccess(JSONArray result) {

                                    }

                                    @Override
                                    public void onError(VolleyError error) {
                                        Intent i = getBaseContext().getPackageManager().getLaunchIntentForPackage(getBaseContext().getPackageName());
                                        i.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                                        startActivity(i);
                                        finish();
                                    }
                                });
                            }
                        })
                        .setNegativeButton("Non", null)
                        .create();
                dialog.show();
                return true;
        }
        return super.onOptionsItemSelected(item);
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.send_menu, menu);

        //Change menu icon color
        Drawable icon = menu.getItem(0).getIcon();
        icon.mutate();
        icon.setColorFilter(getResources().getColor(android.R.color.white), PorterDuff.Mode.SRC_IN);

        return super.onCreateOptionsMenu(menu);
    }
}
