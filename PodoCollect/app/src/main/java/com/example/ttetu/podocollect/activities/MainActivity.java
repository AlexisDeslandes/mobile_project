package com.example.ttetu.podocollect.activities;

import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.PorterDuff;
import android.graphics.drawable.Drawable;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.os.Handler;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.example.ttetu.podocollect.R;
import com.example.ttetu.podocollect.models.Article;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity implements SensorEventListener {

    TextView tv_steps;
    TextView article_text;

    Button nextButton;
    int stepCounter;

    SensorManager sensorManager;

    boolean running = false;
    private int initValue = 0;
    int articleIndex = 0;
    ArrayList<Article> articleList;
    JSONArray stepJsonArray;
    JSONArray stringJsonArray;

    @Override
    public void onBackPressed() {
    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        stepJsonArray = new JSONArray();
        stringJsonArray = new JSONArray();

        articleList = (ArrayList<Article>) getIntent().getSerializableExtra("articleList");

        tv_steps = findViewById(R.id.tv_steps);
        article_text = findViewById(R.id.article_text);

        nextButton = findViewById(R.id.next_button);

        article_text.setText(articleList.get(articleIndex).getName());

        nextButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                    JSONObject articlesString = new JSONObject();
                    JSONObject articlesSteps = new JSONObject();
                    try {
                        if (articleIndex - 1 >= 0) {
                            //Do Nothing
                            articlesSteps.put("startId", articleList.get(articleIndex - 1).getId());
                            articlesSteps.put("endId", articleList.get(articleIndex).getId());
                            articlesSteps.put("distance", stepCounter);
                            stepJsonArray.put(articlesSteps);
                            articlesString.put("startId", articleList.get(articleIndex - 1).getName());
                            articlesString.put("endId", articleList.get(articleIndex).getName());
                            articlesString.put("distance", stepCounter);
                            stringJsonArray.put(articlesString);
                        }else{
                            articlesSteps.put("startId", 1);
                            articlesSteps.put("endId", articleList.get(articleIndex).getId());
                            articlesSteps.put("distance", stepCounter);
                            stepJsonArray.put(articlesSteps);
                            articlesString.put("startId", "Entrée");
                            articlesString.put("endId", articleList.get(articleIndex).getName());
                            articlesString.put("distance", stepCounter);
                            stringJsonArray.put(articlesString);
                        }

                    } catch (JSONException e) {
                        e.printStackTrace();
                    }

                    Log.i("I", "JSON: " + stepJsonArray.toString());

                    stepCounter = 0;
                    initValue = 0;
                    tv_steps.setText(String.valueOf(stepCounter));
                    articleIndex++;
                    if (articleIndex == articleList.size()){
                        article_text.setText(R.string.collect_ended);
                        nextButton.setVisibility(View.INVISIBLE);
                        Log.i("I", "onClick: END");
                        Handler handler = new Handler();
                        handler.postDelayed(new Runnable() {
                            public void run() {
                                // Actions to do after 10 seconds
                                goToEndedCollectActivity(stepJsonArray);
                            }
                        }, 1000);
                        return;
                    }
                    if (articleIndex < articleList.size())
                    article_text.setText(articleList.get(articleIndex).getName());

                }
        });
        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
    }

    @Override
    protected void onResume() {
        super.onResume();
        running = true;
        Sensor countSensor = sensorManager.getDefaultSensor(Sensor.TYPE_STEP_COUNTER);
        if (countSensor != null) {
            sensorManager.registerListener(this, countSensor, SensorManager.SENSOR_DELAY_UI);
        } else {
            Toast.makeText(this, "Sensor Not Found", Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    protected void onPause() {
        super.onPause();
        running = false;
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        //Since it will return the total number since we registered we need to subtract the initial amount
        //for the current steps since we opened app
        if (initValue < 1) {
            // initial value
            initValue = (int) event.values[0];
            //Log.i("i", "onSensorChanged INIT : " + initValue);
        }

        // Calculate steps taken based on first counter value received.
        stepCounter = (int) event.values[0] - initValue;

        if (running) {
            //Log.i("i", "onSensorChanged COUNT : " + stepCounter);
            tv_steps.setText(String.valueOf(stepCounter));
        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int i) {

    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case R.id.action_cancel_collect:
                AlertDialog dialog = new AlertDialog.Builder(this)
                        .setTitle("Annuler la collecte")
                        .setMessage("Etes vous sur de vouloir annuler la collecte ?")
                        .setPositiveButton("Oui", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                goBackToCreateListActivity();
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
        getMenuInflater().inflate(R.menu.collect_menu, menu);

        //Change menu icon color
        Drawable icon = menu.getItem(0).getIcon();
        icon.mutate();
        icon.setColorFilter(getResources().getColor(android.R.color.white), PorterDuff.Mode.SRC_IN);

        return super.onCreateOptionsMenu(menu);
    }

    private void goBackToCreateListActivity() {
        finish();
    }

    private void goToEndedCollectActivity(JSONArray stepJsonArray){
        Intent i = new Intent(this, EndedCollectActivity.class);
        JSONObject distancesJson = new JSONObject();
        try {
            distancesJson.put("token","wakandaforeva");
            distancesJson.put("distances", this.stepJsonArray);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        i.putExtra("distancesJson", distancesJson.toString());
        i.putExtra("stringJsonArray", this.stringJsonArray.toString());
        startActivity(i);
    }

}
