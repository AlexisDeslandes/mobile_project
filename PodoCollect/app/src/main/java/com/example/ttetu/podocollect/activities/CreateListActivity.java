package com.example.ttetu.podocollect.activities;

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
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;

import com.android.volley.VolleyError;
import com.example.ttetu.podocollect.R;
import com.example.ttetu.podocollect.adapters.ArticleListAdapter;
import com.example.ttetu.podocollect.adapters.AutoCompleteListAdapter;
import com.example.ttetu.podocollect.models.Article;
import com.example.ttetu.podocollect.util.Requester;
import com.example.ttetu.podocollect.util.ServerCallBack;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Collections;

import static android.content.Intent.FLAG_ACTIVITY_PREVIOUS_IS_TOP;

public class CreateListActivity extends AppCompatActivity {

    ArticleListAdapter mAdapter;
    ListView articleListView;
    ArrayList<Article> articleList;
    Button startButton;
    Requester r;
    ArrayList<Article> articles;


    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setTheme(R.style.generalnotitle);
        this.setContentView(R.layout.activity_create_list);

        articleListView = findViewById(R.id.article_list);
        startButton = findViewById(R.id.startButton);
        this.articles = new ArrayList<>();
        this.articleList = new ArrayList<>();

        mAdapter = new ArticleListAdapter(this,articleList);
        articleListView.setAdapter(mAdapter);

        startButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Collections.shuffle(articleList);
                openStartActivity();
            }
        });

        r = new Requester(this);
        r.getRequest("http://renaudcosta.pythonanywhere.com/articles", new ServerCallBack() {
             @Override
             public void onSuccess(JSONArray result) {
                 Log.i("I", "onSuccess: " + result.toString());
                 for (int i = 0; i < result.length();i++){
                     try {
                         JSONObject o = result.getJSONObject(i);
                         Article a = new Article(o.getInt("id"),o.getString("nom"));
                         articles.add(a);
                     } catch (JSONException e) {
                         e.printStackTrace();
                     }
                 }
             }

             @Override
             public void onError(VolleyError error) {

             }
         });
    }

    public void openStartActivity() {
        Intent i = new Intent(this, MainActivity.class);
        i.putExtra("articleList",articleList);
        i.setFlags(FLAG_ACTIVITY_PREVIOUS_IS_TOP);
        startActivity(i);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case R.id.action_add_article:
                final Article[] a = new Article[1];
                AutoCompleteListAdapter adapter = new AutoCompleteListAdapter(this, R.layout.auto_complete_row, articles);
                final AutoCompleteTextView articleEditText = new AutoCompleteTextView(this);
                articleEditText.setAdapter(adapter);
                articleEditText.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                    @Override
                    public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                        a[0] = (Article) adapterView.getItemAtPosition(i);
                        articleEditText.setText(a[0].getName());
                    }
                });
                final AlertDialog dialog = new AlertDialog.Builder(this)
                        .setTitle("Ajouter un article")
                        .setView(articleEditText)
                        .setPositiveButton("Ajouter", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                if(articles.contains(a[0]) && !articleList.contains(a[0])){
                                    articleList.add(a[0]);
                                    if (articleList.size() > 1) {
                                        enableStartButton();
                                    }
                                    mAdapter.notifyDataSetChanged();
                                }
                            }
                        })
                        .setNegativeButton("Annuler", null)
                        .create();
                dialog.show();
                return true;
        }
        return super.onOptionsItemSelected(item);
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.list_menu,menu);

        //Change menu icon color
        Drawable icon = menu.getItem(0).getIcon();
        icon.mutate();
        icon.setColorFilter(getResources().getColor(android.R.color.white), PorterDuff.Mode.SRC_IN);

        return super.onCreateOptionsMenu(menu);
    }

    public void deleteArticle(View view){
        View parent = (View)view.getParent();
        TextView articleTextView = parent.findViewById(R.id.article_title);
        Log.e("String", (String) articleTextView.getText());
        String article = String.valueOf(articleTextView.getText());
        for(Article a : articleList){
            if (a.getName().equals(article)){
                articleList.remove(a);
            }
        }
        if(articleList.size() <= 1){
            disableStartButton();
        }
        mAdapter.notifyDataSetChanged();

    }

    private void disableStartButton(){
        startButton.setEnabled(false);
    }

    private void enableStartButton(){
        startButton.setEnabled(true);
    }
}
