package com.example.ttetu.podocollect;

import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.PorterDuff;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.os.PersistableBundle;
import android.support.annotation.Nullable;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;

import java.util.ArrayList;

public class CreateListActivity extends AppCompatActivity {

    ArrayAdapter<String> mAdapter;
    ListView articleListView;
    ArrayList<String> articleList;
    Button startButton;


    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setTheme(R.style.generalnotitle);
        this.setContentView(R.layout.activity_create_list);

        articleListView = findViewById(R.id.article_list);
        startButton = findViewById(R.id.startButton);

        this.articleList = new ArrayList<>();
        mAdapter = new ArrayAdapter<>(this, R.layout.row, R.id.article_title, this.articleList);
        articleListView.setAdapter(mAdapter);

        startButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openStartActivity();
            }
        });

    }

    public void openStartActivity() {
        Intent i = new Intent(this, MainActivity.class);
        startActivity(i);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()){
            case R.id.action_add_article:
                final EditText articleEditText = new EditText(this);
                AlertDialog dialog = new AlertDialog.Builder(this)
                        .setTitle("Ajouter un article")
                        .setView(articleEditText)
                        .setPositiveButton("Ajouter", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                String article = String.valueOf(articleEditText.getText());
                                articleList.add(article);
                                mAdapter.notifyDataSetChanged();
                            }
                        })
                        .setNegativeButton("Annuler",null)
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
        articleList.remove(article);
        mAdapter.notifyDataSetChanged();

    }
}
