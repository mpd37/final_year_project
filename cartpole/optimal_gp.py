import torch
from forwardmodel import ForwardModel, GPModel
from cartpole.utils import get_optimal_gp_inputs, get_optimal_gp_targets
import gpytorch


class OptimalGP(ForwardModel):
    def __init__(self, device):
        super().__init__(get_optimal_gp_inputs(),
                         get_optimal_gp_targets(), D=4, S=5, F=1, device=device)

        self.likelihood = gpytorch.likelihoods.GaussianLikelihood(
            batch_size=self.D).to(self.device)
        self.model = GPModel(self.train_x, self.train_y,
                             self.likelihood).to(self.device)

        self.model.covar_module.outputscale = torch.exp(
            2 * torch.tensor([-0.693683394113827, 0.423507339570434,	1.42772465015533, -0.118724769391329]))

        self.model.likelihood.noise = torch.exp(
            2 * torch.tensor([-4.20208219113606, -4.18403747110293, -3.03665619423097, -4.15544923594675]))

        self.model.covar_module.base_kernel.lengthscale = torch.exp(2 * torch.tensor([
            [[5.09197623441012, 2.55901294199611, 2.51616793809553, 1.56377808915290,
                2.52321937897785, 4.46219125884724]],
            [[5.30712550562476, 4.81695717967186, 2.09823140017308,
                0.373106978222045, -0.15840795786368, 3.14013782905389]],
            [[5.31655750128491, 4.75465061209062, 2.09764048667285,
                0.100758652798785, -0.174452168343103, 3.14470074418502]],
            [[5.23716787507270, 4.83284688416425, 2.71074193002527, 0.760772045870212,
                0.312935572843808, 4.01424840442352]]
        ]))

        self.model.freeze_parameters()
        self.model.eval()
        self.likelihood.eval()

    def learn(self):
        print("Using Optimal GP Model. No training being done.")

        # TO be used for addition of fantasy data
        self.dummy_x = self.train_x
        self.dummy_y = self.train_y

        # Some 'random' computation see ForwardModel for why this might be needed
        self.predict(torch.zeros(1, self.S+self.F, device=self.device))

    def update_data(self, *args, **kwargs):
        pass
