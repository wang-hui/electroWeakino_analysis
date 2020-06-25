int Plot_everything()
{
    bool plot_log = false;
    bool shape_compare = false;
    int rebin = 2; 

    TString results_folder = "";
    TString hist_folder = "plots/";
    TString h_tot_events = "IsSignal_h";

    std::vector<TString> hist_list =
    {
        "AK12JetHeavySDMass_h", "AK12JetLightSDMass_h",
        "AK12JetLepLegSDMass_h", "AK12JetHadLegSDMass_h",
        "AK12JetLepLegTau3Tau1_h", "AK12JetHadLegTau3Tau1_h",
    };

    struct st {TString file; TString name; Color_t color;};

    std::vector<st> struct_list =
    {
        (st){"TTbar_nanoAOD_test", "TTbar", kBlack},
        //(st){"nanoAOD_2017_QCD_HT1000to1500", "QCD", kYellow+1},
        //(st){"nanoAOD_2017_mn1_100_mx1_110", "signal(100,110)", kRed},
        //(st){"nanoAOD_2017_mn1_300_mx1_310", "signal(300,310)", kBlue},
        //(st){"nanoAOD_2017_mn1_300_mx1_350", "signal(300,350)", kGreen},
    };

    for(int i = 0; i < hist_list.size(); i++)
    {
        TString hist_name = hist_list.at(i);
        TString hist = hist_folder + hist_name;

        TCanvas* mycanvas = new TCanvas();
        gStyle->SetOptStat(kFALSE);
        if(plot_log) gPad-> SetLogy();

        TLegend* leg = new TLegend(0.6,0.7,0.89,0.89);
        //leg->SetNColumns(3);
        leg->SetBorderSize(0);
        leg->SetTextSize(0.04);

        float reff = 1E6;
        if(shape_compare) reff = 1;
        float max_y = 0;
        float min_y = 0;

        std::vector<TH1F*> plot_list;

        for(int i = 0; i < struct_list.size(); i++)
        {
            TString f1_name = struct_list.at(i).file; 
            TFile *f1 = new TFile(results_folder + f1_name + "_plots.root");
            TH1F* h1 = (TH1F*)f1->Get(hist);
            h1->Rebin(rebin);
            h1->SetLineColor(struct_list.at(i).color);
            h1->SetLineWidth(2);
            //h1->SetMarkerStyle(20);
            leg->AddEntry(h1,struct_list.at(i).name,"l");
            if(shape_compare) h1->Scale(reff/h1->Integral());
            else
            {
                float f1_tot = ((TH1F*)f1->Get(hist_folder + h_tot_events))->GetEntries();
                h1->Scale(reff/f1_tot);
            }
            plot_list.push_back(h1);
            float h_max = h1->GetMaximum();
            max_y = std::max(max_y, h_max);
        }
        if (plot_log)
        {
            max_y = max_y * 100;
            min_y = 1;
        }
        else max_y = max_y * 1.2;

        for(int i = 0; i < plot_list.size(); i++)
        {
            TH1F* h1 = plot_list.at(i);
            if(i == 0)
            {
                h1->SetMaximum(max_y);
                h1->GetYaxis()->SetRangeUser(min_y, max_y);
                h1->Draw("hist");
            }
            else h1->Draw("histsame");
        }
        leg->Draw("same");

        TString shape_compare_TS = "";
        if(shape_compare) shape_compare_TS = "_shape_comapre";
        mycanvas->SaveAs("plots/" + hist_name + shape_compare_TS + ".png");
    }

    return 0;
}
