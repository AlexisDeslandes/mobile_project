package com.example.ttetu.podocollect.adapters;

import android.annotation.SuppressLint;
import android.content.Context;
import android.support.annotation.NonNull;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import com.example.ttetu.podocollect.R;
import com.example.ttetu.podocollect.models.Article;

import java.util.List;

public class ArticleListAdapter extends ArrayAdapter<Article> {

    public ArticleListAdapter(Context context, List<Article> articles) {
        super(context,0,articles);
    }

    @SuppressLint("SetTextI18n")
    @NonNull
    @Override
    public View getView(int position, View convertView, @NonNull ViewGroup parent) {
        View v = convertView;

        if (v == null) {
            v = LayoutInflater.from(getContext()).inflate(R.layout.row_article,parent,false);
        }

        Article a = getItem(position);

        if (a!=null){
            TextView article = v.findViewById(R.id.article_title);

            if (article != null){
                article.setText(a.getName());
            }
        }
        return v;
    }
}
