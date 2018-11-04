package com.example.ttetu.podocollect.adapters;

import android.content.Context;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Filter;
import android.widget.TextView;

import com.example.ttetu.podocollect.R;
import com.example.ttetu.podocollect.models.Article;

import java.util.ArrayList;
import java.util.List;

public class AutoCompleteListAdapter extends ArrayAdapter {

    private List<Article> dataList;
    private Context mContext;
    private int itemLayout;

    private ListFilter listFilter = new ListFilter();
    private List<Article> dataListAllItems;



    public AutoCompleteListAdapter(Context context, int resource, List<Article> storeDataLst) {
        super(context, resource, storeDataLst);
        dataList = storeDataLst;
        mContext = context;
        itemLayout = resource;
    }

    @Override
    public int getCount() {
        return dataList.size();
    }

    @Override
    public Article getItem(int position) {
        Log.d("AutoCompleteListAdapter",
                dataList.get(position).getName());
        return dataList.get(position);
    }

    @NonNull
    @Override
    public View getView(int position, View view, @NonNull ViewGroup parent) {
        View v = view;
        if (v == null) {
            v = LayoutInflater.from(getContext()).inflate(itemLayout,parent,false);
        }

        Article a = getItem(position);

        assert v != null;
        TextView auto = v.findViewById(R.id.auto_text);

        assert a != null;
        auto.setText(a.getName());

        return v;
    }

    @NonNull
    @Override
    public Filter getFilter() {
        return listFilter;
    }

    public class ListFilter extends Filter {
        private Object lock = new Object();

        @Override
        protected FilterResults performFiltering(CharSequence prefix) {
            FilterResults results = new FilterResults();
            if (dataListAllItems == null) {
                synchronized (lock) {
                    dataListAllItems = new ArrayList<>(dataList);
                }
            }

            if (prefix == null || prefix.length() == 0) {
                synchronized (lock) {
                    results.values = dataListAllItems;
                    results.count = dataListAllItems.size();
                }
            } else {
                final String searchStrLowerCase = prefix.toString().toLowerCase();

                ArrayList<Article> matchValues = new ArrayList<>();

                for (Article dataItem : dataListAllItems){
                    if(dataItem.getName().toLowerCase().startsWith(searchStrLowerCase)){
                        matchValues.add(dataItem);
                    }
                }

                results.values = matchValues;
                results.count = matchValues.size();
            }

            return results;
        }

        @Override
        protected void publishResults(CharSequence constraint, FilterResults results) {
            if (results.values != null) {
                dataList = (ArrayList<Article>)results.values;
            } else {
                dataList = null;
            }
            if (results.count > 0) {
                notifyDataSetChanged();
            } else {
                notifyDataSetInvalidated();
            }
        }

    }
}
