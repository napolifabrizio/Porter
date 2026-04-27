# AWS Infrastructure — Porter

## Overview

Porter roda em uma VPC com separação em subnet pública e privada. O frontend é estático no S3, o backend roda em ECS Fargate na subnet pública (acesso direto ao ECR via internet), e o banco de dados em RDS Aurora PostgreSQL na subnet privada.

---

## VPC Layout

```
VPC
├── Subnet Pública
│   ├── S3 (Frontend estático)
│   └── ECS Fargate (Backend) — acessa ECR via Internet GW
│
└── Subnet Privada
    └── RDS Aurora PostgreSQL
```

---

## Componentes

### Frontend — S3 (Subnet Pública)
- Bucket S3 com hospedagem de site estático
- Acesso público via CloudFront (recomendado) ou diretamente pelo endpoint do S3

### Backend — ECS + Fargate (Subnet Pública)
- Orquestração via ECS
- Runtime serverless via Fargate (sem gerenciamento de EC2)
- Imagens armazenadas no ECR — pull via Internet Gateway (subnet pública)
- **Segurança via SG:** inbound permitido apenas do SG do ALB; nenhuma outra origem aceita

### Banco de Dados — RDS Aurora PostgreSQL (Subnet Privada)
- Acessível apenas pela Subnet Pública (ECS)
- Security Group restrito: aceita tráfego somente na porta 5432 originado do Security Group do ECS
- Sem acesso público

---

## Roteamento

| Route Table  | Associada a     | Destino     | Target           |
|--------------|-----------------|-------------|------------------|
| `rt-public`  | Subnet Pública  | `0.0.0.0/0` | Internet Gateway |
| `rt-private` | Subnet Privada  | local only  | —                |

---

## Security Groups

### SG do ALB (`sg-alb`)
| Direção  | Protocolo | Porta | Origem/Destino |
|----------|-----------|-------|----------------|
| Inbound  | TCP       | 80    | `0.0.0.0/0`    |
| Inbound  | TCP       | 443   | `0.0.0.0/0`    |
| Outbound | TCP       | 8000  | `sg-ecs`       |

### SG do ECS (`sg-ecs`)
| Direção  | Protocolo | Porta | Origem/Destino |
|----------|-----------|-------|----------------|
| Inbound  | TCP       | 8000  | `sg-alb`       |
| Outbound | TCP       | 443   | `0.0.0.0/0` (ECR, internet) |
| Outbound | TCP       | 5432  | `sg-rds`       |

### SG do RDS (`sg-rds`)
| Direção  | Protocolo | Porta | Origem/Destino |
|----------|-----------|-------|----------------|
| Inbound  | TCP       | 5432  | `sg-ecs`       |

---

## Diagrama de Conectividade

```
                        AWS Cloud
┌──────────────────────────────────────────────────────────────┐
│  VPC                                                         │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Subnet Pública                                      │    │
│  │                                                      │    │
│  │   S3 ──────────────────────────────── Internet GW ──┼──► internet
│  │                                                      │    │
│  │   ECS Fargate ──────── ALB (inbound only) ──────────┼──► internet
│  │        │                                             │    │
│  │        └─► Internet GW ──────────────────────────── ┼──► ECR
│  └─────────────────────────────────────────────────────┘    │
│                         │                                    │
│                         │ porta 5432                         │
│                         ▼                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Subnet Privada                                      │    │
│  │   RDS Aurora PostgreSQL                              │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

---

## Por que ECS na Subnet Pública é seguro

- O ECS tem **IP público** mas o SG (`sg-ecs`) bloqueia **todo inbound** exceto do `sg-alb`
- Nenhuma porta está exposta diretamente à internet — todo tráfego externo passa pelo ALB
- O outbound para o ECR funciona via Internet Gateway sem custo de NAT ou VPC Endpoints
- RDS continua isolado na subnet privada, inacessível de fora da VPC

---

## Checklist de Implementação

- [ ] Criar subnet pública com rota `0.0.0.0/0 → Internet Gateway`
- [ ] Criar subnet privada (sem rota para internet)
- [ ] Criar `sg-alb`: inbound 80/443 de `0.0.0.0/0`, outbound 8000 para `sg-ecs`
- [ ] Criar `sg-ecs`: inbound 8000 somente de `sg-alb`, outbound 443 e 5432
- [ ] Criar `sg-rds`: inbound 5432 somente de `sg-ecs`
- [ ] Associar ECS tasks à subnet pública com `sg-ecs`
- [ ] Verificar que a Task Role do ECS tem a policy `AmazonECSTaskExecutionRolePolicy`
- [ ] Verificar que a ECR repository policy permite acesso da conta

---

## Referências

- [ECS Fargate — Networking](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-networking.html)
- [ECR — Pulling images](https://docs.aws.amazon.com/AmazonECR/latest/userguide/pull-through-cache.html)
