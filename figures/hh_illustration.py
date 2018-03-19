import uncertainpy as un
import chaospy as cp
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from HodgkinHuxley import HodgkinHuxley
from prettyplot import prettyPlot, set_xlabel, set_ylabel, get_colormap
from prettyplot import fontsize, labelsize, titlesize, spines_color, set_style


# Logo colors
# Red, Yellow, Grey
colors = [(0.898, 0, 0), (0.976, 0.729, 0.196), (0.259, 0.431, 0.525)]
style = "seaborn-white"
# colors = get_colormap(palette="deep", nr_colors=4)



scale1 = 1.5
scale2 = 0.5
linewidth = 2



###############################
#   Single result             #
###############################



model = HodgkinHuxley()
parameters_3 = {"gbar_Na": scale2*120,
                "gbar_K": scale2*36,
                "gbar_l": scale2*0.5}

time, V, info = model.run(**parameters_3)
prettyPlot(time, V, color=colors[2], style=style, linewidth=linewidth)


set_xlabel("Time (ms)")
set_ylabel("Voltage (mv)")
plt.xlim([0, 23])
plt.xticks([0, 5, 10, 15, 20])
plt.ylim([-80, 43])

plt.savefig("hh_single.png")




###############################
#   Three different results   #
###############################


parameters_1 = {"gbar_Na": 120,
                "gbar_K": 36,
                "gbar_l": 0.5}


time, V, info = model.run(**parameters_1)
prettyPlot(time, V, color=colors[1], style=style, linewidth=linewidth)


parameters_2 = {"gbar_Na": scale1*120,
                "gbar_K": scale1*36,
                "gbar_l": scale1*0.5}

time, V, info = model.run(**parameters_2)
prettyPlot(time, V, new_figure=False, color=colors[0], style=style, linewidth=linewidth)



parameters_3 = {"gbar_Na": scale2*120,
                "gbar_K": scale2*36,
                "gbar_l": scale2*0.5}

time, V, info = model.run(**parameters_3)
prettyPlot(time, V, new_figure=False, color=colors[2], style=style, linewidth=linewidth)

set_xlabel("Time (ms)")
set_ylabel("Voltage (mv)")
plt.xlim([0, 23])
plt.xticks([0, 5, 10, 15, 20])
plt.ylim([-80, 43])
plt.savefig("hh.png")
plt.savefig("hh.pdf")
# plt.show()


###############################
#   Large variance            #
###############################

# Large variance

# # Define a parameter list
# parameter_list = [["gbar_Na", 120],
#                   ["gbar_K", 36],
#                   ["gbar_l", 0.3]]

# # Create the parameters
# parameters = un.Parameters(parameter_list)

# # Set all parameters to have a uniform distribution
# # within a 25% interval around their fixed value
# parameters.set_all_distributions(un.uniform(0.25))


# parameters = {"gbar_Na": cp.Uniform(100, 140),     # 120
#               "gbar_K": cp.Uniform(32, 40),        # 36
#               "gbar_l": cp.Uniform(0.2, 0.4)}      # 0.3

parameters = {"gbar_Na": cp.Uniform(60, 180),       # 120
              "gbar_K": cp.Uniform(18, 54),         # 36
              "gbar_l": cp.Uniform(0.15, 0.45)}     # 0.3

# Initialize the model
model = HodgkinHuxley()

# Perform the uncertainty quantification
UQ = un.UncertaintyQuantification(model=model,
                                  parameters=parameters)
data = UQ.quantify(plot=None, nr_pc_mc_samples=10**3, save=False)




###############################
#   Plot prediction interval  #
###############################

time = data["HodgkinHuxley"].time
mean = data["HodgkinHuxley"].mean
variance = data["HodgkinHuxley"].variance
percentile_95 = data["HodgkinHuxley"].percentile_95
percentile_5 = data["HodgkinHuxley"].percentile_5
sobol = data["HodgkinHuxley"].sobol_first

ax = prettyPlot(time, mean, color=colors[2], palette="deep", linewidth=2, style=style)

ax.set_ylabel(r"Mean (mV)", fontsize=labelsize)
ax.set_xlabel("Time (ms)", fontsize=labelsize)


ax.fill_between(time,
                percentile_5,
                percentile_95,
                color=colors[2],
                alpha=0.6,
                linewidth=0)

plt.xlim([0, 23])
plt.xticks([0, 5, 10, 15, 20])

plt.savefig("hh_prediction.png")
plt.savefig("hh_prediction.pdf")
# plt.show()



###############################
#   Plot mean and variance    #
###############################




ax = prettyPlot(time, mean, color=colors[0], palette="deep", linewidth=2, style="seaborn-white")
ax.set_ylabel(r"Mean (mV)", fontsize=labelsize, color=colors[0])
ax.tick_params(axis="y", which="both", right="off", labelright="off", labelcolor=colors[0])
ax.set_xlabel("Time (ms)", fontsize=labelsize, color="black")
ax.spines["left"].set_edgecolor(colors[0])

ax.tick_params(axis="y", which="both", right="off", left="on", labelleft="on",
               color=colors[0], labelcolor=colors[0], labelsize=labelsize)


ax2 = ax.twinx()
ax2.plot(time, variance, color=colors[2], linewidth=2)
ax2.grid(False)

ax2.spines["left"].set_edgecolor(colors[0])

ax2.spines["right"].set_visible(True)
ax2.spines["right"].set_edgecolor(colors[2])
ax2.patch.set_visible(False)
ax2.tick_params(axis="x", labelbottom="off")

ax2.tick_params(axis="y", which="both", right="on", left="off", labelright="on", labelleft="off",
                color=colors[2], labelcolor=colors[2], labelsize=labelsize)

ax2.set_ylabel(r"Variance ($\mathrm{mV}^2$)", color=colors[2], fontsize=labelsize)
plt.savefig("hh_mean.png")



###############################
#   Plot sensitivity          #
###############################



ax = prettyPlot(time, sobol[0], color=colors[0], palette="deep", linewidth=2,
           style=style)

ax.set_ylabel(r"Sensitivity", fontsize=labelsize)
ax.set_xlabel("Time (ms)", fontsize=labelsize)
ax.set_ylim([0, 1])
ax.set_xlim([min(time), max(time)])

plt.savefig("sensitivity.png")



###############################
#   Plot sensitivity and mean #
###############################


ax = prettyPlot(time, sobol[0], color=colors[0], palette="deep", linewidth=2, style="seaborn-white")
ax.set_ylabel(r"Sensitivity", fontsize=labelsize, color=colors[0])
ax.tick_params(axis="y", which="both", right="off", labelright="off", labelcolor=colors[0])
ax.set_xlabel("Time (ms)", fontsize=labelsize, color="black")
ax.spines["left"].set_edgecolor(colors[0])
ax.set_xlim([min(time), max(time)])


ax.tick_params(axis="y", which="both", right="off", left="on", labelleft="on",
               color=colors[0], labelcolor=colors[0], labelsize=labelsize)


ax2 = ax.twinx()
ax2.plot(time, data["HodgkinHuxley"].evaluations[0], color=colors[2], linewidth=2)
ax2.grid(False)

ax2.spines["left"].set_edgecolor(colors[0])

ax2.spines["right"].set_visible(True)
ax2.spines["right"].set_edgecolor(colors[2])
ax2.patch.set_visible(False)
ax2.tick_params(axis="x", labelbottom="off")

ax2.tick_params(axis="y", which="both", right="on", left="off", labelright="on", labelleft="off",
                color=colors[2], labelcolor=colors[2], labelsize=labelsize)

ax2.set_ylabel(r"Membrane potential (mV)", color=colors[2], fontsize=labelsize)

ax.set_ylim([0, 1])
plt.savefig("sensitivity_mean.png")



###############################
#   Plot all sensitivity      #
###############################


titles = [r"Potassium conductance $\bar{g}_\mathrm{K}$", r"Sodium conductance $\bar{g}_\mathrm{Na}$", r"Leak conductance $\bar{g}_\mathrm{l}$"]
nr_plots = len(data.uncertain_parameters)
grid_size = np.ceil(np.sqrt(nr_plots))
grid_x_size = int(grid_size)
grid_y_size = int(np.ceil(nr_plots/float(grid_x_size)))

fig, axes = plt.subplots(nrows=grid_y_size, ncols=grid_x_size, squeeze=False,
                         sharex="col", sharey="row")


labels = data.get_labels("HodgkinHuxley")
xlabel, ylabel = labels

set_style("seaborn-white")
ax = fig.add_subplot(111, zorder=-10)
spines_color(ax, edges={"top": "None", "bottom": "None",
                        "right": "None", "left": "None"})
ax.tick_params(labelcolor="w", top="off", bottom="off", left="off", right="off")
ax.set_xlabel(xlabel.capitalize(), labelpad=8)
ax.set_ylabel("Sensitivity", labelpad=8)

for i in range(0, grid_x_size*grid_y_size):
    nx = i % grid_x_size
    ny = int(np.floor(i/float(grid_x_size)))

    ax = axes[ny][nx]

    if i < nr_plots:
        title = titles[i]

        prettyPlot(time, sobol[i],
                color=colors[i],
                ax=ax,
                linewidth=linewidth,
                style=style)

        ax.set_title(title, fontsize=14)

        ax.set_ylim([-0.0, 1.0])
        ax.set_xlim([min(time), max(time)])
        ax.tick_params(labelsize=fontsize)
        ax.set_yticks([0, 0.5, 1])
    else:
        ax.axis("off")

plt.tight_layout()
plt.savefig("sensitivity_all.png")
