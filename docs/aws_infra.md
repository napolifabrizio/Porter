# AWS Infrastructure — Porter

## Overview

Porter roda em uma VPC com separação em subnets pública e privadas. O frontend é estático no S3, o backend roda em ECS Fargate, e o banco de dados em RDS Aurora PostgreSQL.

---

## VPC Layout

```
VPC
├── Subnet Pública
│   └── S3 (Frontend estático)
│
├── Subnet Privada 1
│   └── ECS Fargate (Backend)
│
└── Subnet Privada 2
    └── RDS Aurora PostgreSQL
```

---

## Componentes

### Frontend — S3 (Subnet Pública)
- Bucket S3 com hospedagem de site estático
- Acesso público via CloudFront (recomendado) ou diretamente pelo endpoint do S3
- Nenhuma rota de saída especial necessária

### Backend — ECS + Fargate (Subnet Privada 1)
- Orquestração via ECS
- Runtime serverless via Fargate (sem gerenciamento de EC2)
- Imagens armazenadas no ECR
- Sem acesso direto à internet

### Banco de Dados — RDS Aurora PostgreSQL (Subnet Privada 2)
- Acessível apenas pela Subnet Privada 1 (ECS)
- Security Group restrito: aceita tráfego somente na porta 5432 originado do Security Group do ECS
- Sem acesso público

---

## Roteamento

| Route Table         | Associada a                          | Destino          | Target              |
|---------------------|--------------------------------------|------------------|---------------------|
| `rt-public`         | Subnet Pública                       | `0.0.0.0/0`      | Internet Gateway    |
| `rt-private`        | Subnet Privada 1 + Subnet Privada 2  | local only       | —                   |

> A `rt-private` atualmente **não tem rota para internet**. Ver seção de VPC Endpoints abaixo.

---

## Pergunta: Como o ECS puxa imagens do ECR sem internet?

### Opção A — NAT Gateway (não recomendada para este caso)

Adicionar um NAT Gateway na subnet pública e uma rota `0.0.0.0/0 → NAT GW` na `rt-private`.

**Problema:** custo fixo de ~$32/mês + cobrança por GB de dados transferidos. Desnecessário se o único motivo for acessar o ECR.

---

### Opção B — VPC Endpoints (recomendada) ✅

VPC Endpoints (PrivateLink) criam um caminho privado entre sua VPC e serviços AWS **sem sair para a internet** e sem custo de NAT.

#### Endpoints necessários para ECS Fargate + ECR

| Endpoint                                  | Tipo      | Motivo                                                     |
|-------------------------------------------|-----------|------------------------------------------------------------|
| `com.amazonaws.{region}.ecr.dkr`          | Interface | Pull das imagens Docker                                    |
| `com.amazonaws.{region}.ecr.api`          | Interface | Autenticação e chamadas à API do ECR                       |
| `com.amazonaws.{region}.s3`               | Gateway   | ECR armazena as layers das imagens no S3 (gratuito)        |
| `com.amazonaws.{region}.logs`             | Interface | CloudWatch Logs (obrigatório se usar `awslogs` log driver) |
| `com.amazonaws.{region}.ecs`              | Interface | ECS control plane                                          |
| `com.amazonaws.{region}.ecs-agent`        | Interface | ECS agent (Fargate)                                        |
| `com.amazonaws.{region}.ecs-telemetry`    | Interface | Métricas do ECS agent                                      |

#### Configuração dos Endpoints de Interface
- Criar na **Subnet Privada 1** (onde o ECS roda)
- Associar um Security Group que permita **HTTPS (443) inbound** da própria subnet
- Habilitar **Private DNS** em cada endpoint

#### Configuração do Endpoint Gateway (S3)
- Associar à `rt-private` — ele injeta a rota automaticamente, sem custo adicional

#### Custo dos Interface Endpoints
- ~$0.01/hora por endpoint × número de AZs ≈ ~$7/mês por endpoint
- Para os 3 endpoints essenciais (ecr.dkr, ecr.api, logs): ~$21/mês — ainda mais barato que NAT Gateway para cargas baixas

---

## Fluxo de Pull de Imagem (com VPC Endpoints)

```
ECS Fargate Task (Subnet Privada 1)
    │
    ├─► ecr.api endpoint  →  autentica no ECR
    │
    ├─► ecr.dkr endpoint  →  obtém manifesto da imagem
    │
    └─► S3 Gateway endpoint  →  baixa as layers da imagem
```

Todo o tráfego permanece dentro da rede AWS. Nenhum pacote atravessa a internet.

---

## Security Groups — Regras Recomendadas

### SG do ECS (`sg-ecs`)
| Direção  | Protocolo | Porta | Origem/Destino        |
|----------|-----------|-------|-----------------------|
| Outbound | TCP       | 443   | `pl-xxxxx` (S3 prefix list) |
| Outbound | TCP       | 443   | Subnet Privada 1 CIDR (para os endpoints) |
| Outbound | TCP       | 5432  | `sg-rds`              |

### SG do RDS (`sg-rds`)
| Direção  | Protocolo | Porta | Origem/Destino |
|----------|-----------|-------|----------------|
| Inbound  | TCP       | 5432  | `sg-ecs`       |

### SG dos VPC Endpoints (`sg-vpce`)
| Direção  | Protocolo | Porta | Origem/Destino       |
|----------|-----------|-------|----------------------|
| Inbound  | TCP       | 443   | Subnet Privada 1 CIDR |

---

## Diagrama de Conectividade

```
                        AWS Cloud
┌──────────────────────────────────────────────────────────────┐
│  VPC                                                         │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Subnet Pública                                      │    │
│  │   S3 ──────────────────────────────── Internet GW   │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Subnet Privada 1                                    │    │
│  │                                                      │    │
│  │   ECS Fargate ──┬─► VPC Endpoint (ecr.dkr)  ──► ECR│    │
│  │                 ├─► VPC Endpoint (ecr.api)   ──► ECR│    │
│  │                 ├─► S3 Gateway Endpoint      ──► S3 │    │
│  │                 └─► VPC Endpoint (logs)      ──► CW │    │
│  └─────────────────────────────────────────────────────┘    │
│                         │                                    │
│                         │ porta 5432                         │
│                         ▼                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Subnet Privada 2                                    │    │
│  │   RDS Aurora PostgreSQL                              │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

---

## Checklist de Implementação

- [ ] Criar VPC Endpoint Interface: `ecr.dkr`
- [ ] Criar VPC Endpoint Interface: `ecr.api`
- [ ] Criar VPC Endpoint Gateway: `s3` e associar à `rt-private`
- [ ] Criar VPC Endpoint Interface: `logs` (se usar CloudWatch)
- [ ] Habilitar **Private DNS** em todos os endpoints de interface
- [ ] Criar `sg-vpce` permitindo HTTPS inbound da Subnet Privada 1
- [ ] Verificar que a Task Role do ECS tem a policy `AmazonECSTaskExecutionRolePolicy`
- [ ] Verificar que a ECR repository policy permite acesso da conta

---

## Referências

- [ECS Fargate — VPC Endpoints required](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/vpc-endpoints.html)
- [ECR — Interface VPC Endpoints](https://docs.aws.amazon.com/AmazonECR/latest/userguide/vpc-endpoints.html)
- [Pricing: VPC PrivateLink](https://aws.amazon.com/privatelink/pricing/)
