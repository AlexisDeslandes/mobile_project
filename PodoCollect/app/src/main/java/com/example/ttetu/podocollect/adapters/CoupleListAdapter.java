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
import com.example.ttetu.podocollect.models.ArticleCouple;

import java.util.List;

public class CoupleListAdapter extends ArrayAdapter<ArticleCouple> {

    public CoupleListAdapter(Context context, List<ArticleCouple> couples) {
        super(context,0,couples);
    }

    @SuppressLint("SetTextI18n")
    @NonNull
    @Override
    public View getView(int position, View convertView, @NonNull ViewGroup parent) {
        View v = convertView;

        if (v == null) {
            v = LayoutInflater.from(getContext()).inflate(R.layout.row_collect,parent,false);
        }

        ArticleCouple c = getItem(position);

        if (c!=null){
            TextView articles = v.findViewById(R.id.articles);
            TextView steps = v.findViewById(R.id.nb_steps_text);

            if (articles != null){
                articles.setText(c.getStart() + " → " + c.getEnd());
            }
            
            if (steps != null){
                steps.setText(String.valueOf(c.getSteps()));
            }
        }
        return v;
    }
}
